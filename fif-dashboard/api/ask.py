"""Vercel serverless function: POST /api/ask  ->  {"answer": "..."}

The page (rag.js) sends {"question", "character", "context":[{text}], "task", "history"}; this asks an
OpenAI-compatible chat model and returns the answer. The API key lives ONLY in Vercel environment variables.

Vercel -> Project -> Settings -> Environment Variables:
    LLM_BASE_URL    e.g. https://api.groq.com/openai/v1   (your provider's OpenAI-compatible base URL)
    LLM_API_KEY     your key
    LLM_MODEL       exact model id from YOUR provider's model list
    ALLOWED_ORIGIN  your site, e.g. https://my-site.vercel.app   (comma-separate several; leave empty = any)

Then in content/chat.json:  "api_url": "/api/ask"   (same Vercel project)  or the full https://.../api/ask URL.
"""
from __future__ import annotations

import json
import os
import re
import sys
from http.server import BaseHTTPRequestHandler
from urllib import error, request

BASE = os.environ.get("LLM_BASE_URL", "").rstrip("/")
KEY = os.environ.get("LLM_API_KEY", "")
MODEL = os.environ.get("LLM_MODEL", "")
ALLOWED = [o.strip().rstrip("/") for o in os.environ.get("ALLOWED_ORIGIN", "").split(",") if o.strip()]
MAX_CHUNKS, MAX_CHARS = 6, 1500

NO_LEAKS = (
    "Never mention how the data is stored or prepared: no file names, document or section titles, passage numbers, "
    "table or column names, row counts, removed duplicates or other cleaning steps. Talk about the science and the findings, not the files. "
)

SYSTEM = (
    "You are a crew member in an educational site about NASA microgravity fire experiments. "
    "Answer the question using ONLY the context passages. Do not use outside knowledge and never invent numbers. "
    + NO_LEAKS +
    "If the question uses words like 'it', 'that' or 'more', use the earlier conversation only to work out what they refer to; "
    "the facts still come only from the passages. "
    "If the passages answer only part of the question, give that part and say what is missing. "
    "Only if they contain nothing relevant, reply exactly: \"That is not in our data.\" "
    "Keep the answer to 2-4 short sentences in plain language."
)

SYSTEM_SUMMARY = (
    "You are a crew member in an educational site about NASA microgravity fire experiments. "
    "Summarize the numbered context passages in 3-5 short sentences of plain language. Use ONLY the passages and never invent numbers. "
    + NO_LEAKS +
    "Say what was tested and what was learned. Do not describe the layout of tables or list their columns or settings."
)

SYSTEM_GENERAL = (
    "You are a friendly crew member in an educational site about NASA microgravity fire experiments. "
    "The visitor's question is not in our texts. If it is a simple, general-knowledge question that fits this theme "
    "(space, spacecraft, the space station, cargo vehicles, fire and combustion, physics, basic science and engineering terms), "
    "answer it in 1-3 short sentences of plain language using well-established general knowledge. "
    "Do not quote numbers from NASA experiments and do not say the answer comes from our data. "
    "If the question is not about this theme, or you are not sure, reply exactly: \"That is not in our data.\""
)


def history_messages(body: dict) -> list[dict]:
    out = []
    for h in (body.get("history") or [])[-3:]:
        if not isinstance(h, dict):
            continue
        q, a = str(h.get("q", ""))[:300], str(h.get("a", ""))[:400]
        if q and a:
            out += [{"role": "user", "content": q}, {"role": "assistant", "content": a}]
    return out


def build_messages(body: dict) -> list[dict]:
    q = str(body.get("question", ""))[:300]
    task = body.get("task")
    if task == "general":
        return [{"role": "system", "content": SYSTEM_GENERAL}] + history_messages(body) + [{"role": "user", "content": q}]
    # only the passage text is shown to the model: no topic, file or title names it could repeat
    parts = [f"[{i}]\n{str(c.get('text', ''))[:MAX_CHARS]}" for i, c in enumerate((body.get("context") or [])[:MAX_CHUNKS], 1)]
    if task == "summary":
        user = "Context:\n\n" + "\n\n".join(parts) + "\n\nTask: write a short summary (3-5 sentences) of what these passages say, covering the different topics."
        return [{"role": "system", "content": SYSTEM_SUMMARY}, {"role": "user", "content": user}]
    user = "Context:\n\n" + "\n\n".join(parts) + f"\n\nQuestion: {q}"
    return [{"role": "system", "content": SYSTEM}] + history_messages(body) + [{"role": "user", "content": user}]


# safety net: even if the model slips, sentences about files / tables / cleaning never reach the page
LEAK = re.compile(r"(\b\d[\d,]*\s+(?:data\s+)?rows?\b|\bduplicates?\b|\b(?:original|source|data) table\b|"
                  r"\b[\w\-]+\.(?:txt|csv|json|pdf|md|xlsx?|docx?)\b|\bPSI-\d+\w*)", re.I)


def clean(text: str) -> str:
    text = re.sub(r"\s*\[\d+\]|\bpassages?\s+\d+\b", "", text, flags=re.I)
    kept = [s for s in re.split(r"(?<=[.!?])\s+", text) if not LEAK.search(s)]
    return " ".join(kept).strip()


def ask_llm(messages: list[dict]) -> str:
    payload = json.dumps({"model": MODEL, "messages": messages, "temperature": 0.2, "max_tokens": 1200}).encode()
    headers = {"Content-Type": "application/json", "Accept": "application/json",
               "User-Agent": "fif-dashboard/1.0 (+local proxy)"}   # the default Python-urllib agent is blocked by some providers (403)
    if KEY:
        headers["Authorization"] = f"Bearer {KEY}"
    req = request.Request(f"{BASE}/chat/completions", data=payload, headers=headers, method="POST")
    with request.urlopen(req, timeout=25) as r:
        text = json.loads(r.read())["choices"][0]["message"].get("content") or ""
    text = re.sub(r"<think>.*?</think>", "", text, flags=re.S).strip()   # some reasoning models print their thinking
    text = clean(text)
    if not text:
        raise ValueError("empty answer")                                   # page falls back to the offline answer
    return text


class handler(BaseHTTPRequestHandler):
    def _origin_ok(self) -> bool:
        origin = self.headers.get("Origin", "").rstrip("/")
        return not ALLOWED or not origin or origin in ALLOWED      # same-origin calls send no Origin header

    def _send(self, code: int, obj: dict | None = None):
        self.send_response(code)
        origin = self.headers.get("Origin", "").rstrip("/")
        if not ALLOWED:
            self.send_header("Access-Control-Allow-Origin", "*")
        elif origin in ALLOWED:
            self.send_header("Access-Control-Allow-Origin", origin)
            self.send_header("Vary", "Origin")
        self.send_header("Access-Control-Allow-Methods", "POST, GET, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        data = json.dumps(obj or {}).encode()
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_OPTIONS(self):
        self._send(204)

    def do_GET(self):                                               # open /api/ask in a browser to check it is deployed
        self._send(200, {"ok": True, "configured": bool(BASE and MODEL)})

    def do_POST(self):
        if not self._origin_ok():
            return self._send(403, {"error": "origin not allowed"})
        if not (BASE and MODEL):
            print("LLM_BASE_URL / LLM_MODEL are not set in the Vercel environment variables", file=sys.stderr)
            return self._send(500, {"error": "not configured"})
        try:
            n = int(self.headers.get("Content-Length", 0))
            if n > 100_000:
                return self._send(413, {"error": "too large"})
            body = json.loads(self.rfile.read(n))
            if not body.get("context") and body.get("task") != "general":
                return self._send(200, {"answer": "That is not in our data."})
            self._send(200, {"answer": ask_llm(build_messages(body))})
        except (error.URLError, error.HTTPError, KeyError, ValueError, TimeoutError) as e:
            detail = ""
            if isinstance(e, error.HTTPError):
                try:
                    detail = " | " + e.read().decode("utf-8", "replace")[:300]
                except Exception:
                    pass
            print("upstream error:", repr(e) + detail, file=sys.stderr)   # details stay in the Vercel logs, not the page
            self._send(502, {"error": "model unavailable"})

    def log_message(self, fmt, *a):
        pass
