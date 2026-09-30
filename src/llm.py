import json
import os
import re
from typing import Any, Dict, Optional

try:
    from groq import Groq
except ImportError:  # pragma: no cover
    Groq = None

DEFAULT_MODEL = os.getenv("GROQ_MODEL", "openai/gpt-oss-20b")


def _extract_json(text: str) -> Dict[str, Any]:
    """Extract a JSON object from an LLM response."""
    text = text.strip()
    if text.startswith("```"):
        text = re.sub(r"^```(?:json)?\s*", "", text, flags=re.I)
        text = re.sub(r"\s*```$", "", text)
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        match = re.search(r"\{.*\}", text, flags=re.DOTALL)
        if match:
            return json.loads(match.group(0))
        raise


def is_live_mode() -> bool:
    return bool(os.getenv("GROQ_API_KEY")) and Groq is not None


def chat(system_prompt: str, user_prompt: str, temperature: float = 0.2) -> str:
    """Call Groq when configured; raise a clear error otherwise."""
    if not is_live_mode():
        raise RuntimeError("GROQ_API_KEY is not configured. Use Demo Mode or add an API key.")

    client = Groq(api_key=os.environ["GROQ_API_KEY"])
    response = client.chat.completions.create(
        model=DEFAULT_MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        temperature=temperature,
    )
    return response.choices[0].message.content or ""


def chat_json(system_prompt: str, user_prompt: str) -> Dict[str, Any]:
    raw = chat(system_prompt, user_prompt, temperature=0.1)
    return _extract_json(raw)
