import os
from typing import Any

from openai import OpenAI


class NemotronAgent:
    """Thin adapter around the OpenAI-compatible Nebius Token Factory API."""

    def __init__(self) -> None:
        api_key = os.getenv("NEBIUS_API_KEY")
        base_url = os.getenv(
            "NEBIUS_BASE_URL",
            "https://api.tokenfactory.nebius.com/v1/",
        )
        model = os.getenv("NEMOTRON_MODEL")

        if not api_key:
            raise RuntimeError("NEBIUS_API_KEY is not configured.")
        if not model:
            raise RuntimeError("NEMOTRON_MODEL is not configured.")

        self.model = model
        self.client = OpenAI(api_key=api_key, base_url=base_url)

    def reason(self, readiness_context: dict[str, Any], goal: str) -> str:
        system_prompt = (
            "You are the reasoning layer of RADEM HUTIS, a human-centric "
            "transformation intelligence system. Analyze only the supplied "
            "readiness context. Produce concise, explainable decision-support "
            "guidance. Do not invent missing assessment facts."
        )

        user_prompt = (
            f"Goal: {goal}\n\n"
            f"Readiness context: {readiness_context}\n\n"
            "Return: (1) key readiness signals, (2) main transformation gaps, "
            "(3) a prioritized adaptive roadmap, and (4) measurable follow-up indicators."
        )

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0.2,
        )

        return response.choices[0].message.content or ""
