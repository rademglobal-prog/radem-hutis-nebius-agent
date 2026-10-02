import json
import os
import time
from datetime import datetime, timezone
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

API_KEY = os.getenv("NEBIUS_API_KEY")
BASE_URL = os.getenv("NEBIUS_BASE_URL", "https://api.tokenfactory.nebius.com/v1/")
MODEL = os.getenv("NEMOTRON_MODEL", "nvidia/Nemotron-3_5-Lightning")

if not API_KEY:
    raise SystemExit("NEBIUS_API_KEY is not configured.")

client = OpenAI(api_key=API_KEY, base_url=BASE_URL)

messages = [
    {
        "role": "system",
        "content": (
            "You are the reasoning layer of RADEM HUTIS. "
            "Analyze only the supplied readiness context. "
            "Give concise, explainable decision-support guidance."
        ),
    },
    {
        "role": "user",
        "content": (
            "Readiness dimensions: awareness=72, acceptance=61, capacity=58, "
            "alignment=66, sustainability=55. "
            "Generate: 1) key readiness signals, 2) main transformation gaps, "
            "3) a prioritized three-step roadmap, 4) measurable follow-up indicators."
        ),
    },
]

started = time.perf_counter()
response = client.chat.completions.create(
    model=MODEL,
    messages=messages,
    temperature=0.2,
)
elapsed = time.perf_counter() - started

usage = response.usage
prompt_tokens = getattr(usage, "prompt_tokens", None) if usage else None
completion_tokens = getattr(usage, "completion_tokens", None) if usage else None
total_tokens = getattr(usage, "total_tokens", None) if usage else None
tokens_per_second = (
    round(completion_tokens / elapsed, 2)
    if completion_tokens is not None and elapsed > 0
    else None
)

result = {
    "timestamp_utc": datetime.now(timezone.utc).isoformat(),
    "model": MODEL,
    "base_url": BASE_URL,
    "elapsed_seconds": round(elapsed, 3),
    "prompt_tokens": prompt_tokens,
    "completion_tokens": completion_tokens,
    "total_tokens": total_tokens,
    "completion_tokens_per_second": tokens_per_second,
    "response": response.choices[0].message.content,
}

Path("benchmarks").mkdir(exist_ok=True)
out = Path("benchmarks/latest.json")
out.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")

print(json.dumps(result, ensure_ascii=False, indent=2))
print(f"\nSaved benchmark to {out}")
