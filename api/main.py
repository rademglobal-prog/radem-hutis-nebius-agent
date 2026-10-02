from typing import Any

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from agents.nemotron_agent import NemotronAgent

load_dotenv()

app = FastAPI(
    title="RADEM HUTIS Nebius Agent",
    version="0.1.0",
    description="Hackathon API adapter for HUTIS reasoning with Nebius Token Factory and NVIDIA Nemotron.",
)


class ReasonRequest(BaseModel):
    readiness_context: dict[str, Any] = Field(
        ...,
        description="Structured HUTIS readiness context. Do not send secrets.",
    )
    goal: str = Field(
        default="Generate an adaptive transformation roadmap.",
        min_length=3,
        max_length=1000,
    )


class ReasonResponse(BaseModel):
    model: str
    result: str


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/v1/reason", response_model=ReasonResponse)
def reason(payload: ReasonRequest) -> ReasonResponse:
    try:
        agent = NemotronAgent()
        result = agent.reason(payload.readiness_context, payload.goal)
        return ReasonResponse(model=agent.model, result=result)
    except RuntimeError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    except Exception as exc:
        # Do not expose provider credentials or raw authorization data.
        raise HTTPException(
            status_code=502,
            detail="The external reasoning provider request failed.",
        ) from exc
