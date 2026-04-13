"""Minimal client for a local LLM served by Ollama.

Default endpoint: http://localhost:11434/api/chat
"""

import requests


OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL = "llama3.1:8b"


def chat(messages, model=MODEL, url=OLLAMA_URL, temperature=0):
    payload = {
        "model": model,
        "messages": messages,
        "stream": False,
        "options": {"temperature": temperature},
    }
    response = requests.post(url, json=payload, timeout=120)
    response.raise_for_status()
    data = response.json()
    return data["message"]["content"]
