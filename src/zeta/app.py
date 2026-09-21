from __future__ import annotations

import json
import os
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field


ROOT = Path(__file__).parent
app = FastAPI(title="Zeta Chat", version="0.2.0")


class Message(BaseModel):
    role: str = Field(pattern="^(user|assistant|system)$")
    content: str = Field(min_length=1, max_length=12_000)


class ChatRequest(BaseModel):
    messages: list[Message] = Field(min_length=1, max_length=50)


def demo_response(messages: list[Message]) -> str:
    """Provide a useful local response when no model key is configured."""
    prompt = next((m.content for m in reversed(messages) if m.role == "user"), "hello")
    return (
        "Zeta is running in demo mode because OPENAI_API_KEY is not configured. "
        f"You said: {prompt}\n\nAdd an API key to connect Zeta to a real model."
    )


def model_response(messages: list[Message]) -> str:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return demo_response(messages)

    base_url = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1").rstrip("/")
    payload = json.dumps(
        {
            "model": os.getenv("ZETA_MODEL", "gpt-4o-mini"),
            "messages": [message.model_dump() for message in messages],
            "temperature": 0.7,
        }
    ).encode()
    request = Request(
        f"{base_url}/chat/completions",
        data=payload,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    try:
        with urlopen(request, timeout=90) as response:
            result = json.loads(response.read().decode())
        return result["choices"][0]["message"]["content"]
    except (HTTPError, URLError, KeyError, IndexError, json.JSONDecodeError) as exc:
        raise HTTPException(status_code=502, detail="The AI provider could not be reached.") from exc


@app.get("/", response_class=FileResponse)
def index() -> Path:
    return ROOT / "static" / "index.html"


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "mode": "live" if os.getenv("OPENAI_API_KEY") else "demo"}


@app.post("/api/chat")
def chat(request: ChatRequest) -> dict[str, str]:
    return {"message": model_response(request.messages)}
