# RADEM HUTIS Nebius Agent

Human Transformation Intelligence agent for the **Nebius x NVIDIA Global AI Hackathon 2026**.

RADEM HUTIS is a human-centric transformation intelligence prototype that turns readiness assessment data into structured reasoning, adaptive transformation guidance, and follow-up measurement.

> **Build status:** hackathon integration in progress. The repository contains the integration layer for Nebius Token Factory / NVIDIA Nemotron. Runtime benchmark results and the final selected Nemotron model will be documented only after live testing.

## Workflow

```text
Assessment
   ↓
Readiness Analysis
   ↓
HUTIS Context Builder
   ↓
Nebius Token Factory
   ↓
NVIDIA Nemotron Reasoning
   ↓
Adaptive Transformation Roadmap
   ↓
Measurement / Follow-up
```

## Why Nebius + NVIDIA Nemotron

The hackathon extension uses the **OpenAI-compatible Nebius Token Factory inference API** as the model gateway and is designed to use an **NVIDIA Nemotron open model** for reasoning over structured HUTIS readiness context.

The current first-pass candidate is `nvidia/Nemotron-3_5-Lightning`, while `NEMOTRON_MODEL` remains configurable so additional Nemotron variants can be benchmarked without changing application code.

## Authentication and credential handling

This repository does **not** contain API keys.

- `NEBIUS_API_KEY` is read from the process environment.
- `.env` is excluded by `.gitignore`.
- `.env.example` contains variable names only, never secrets.
- The OpenAI-compatible client sends the API key as the authorization credential to the configured Nebius Token Factory endpoint.
- No end-user password database, session cookie, or locally persisted access token is used in this prototype.

See [docs/AUTHENTICATION.md](docs/AUTHENTICATION.md) for the request flow and security model.

## Project structure

```text
api/
  main.py                  FastAPI HTTP interface
agents/
  nemotron_agent.py        Nebius/Nemotron inference adapter
docs/
  ARCHITECTURE.md          System architecture
  AUTHENTICATION.md        Credentials and request flow
.env.example               Environment variable template
requirements.txt           Python dependencies
```

## Setup

### 1. Clone

```bash
git clone https://github.com/rademglobal-prog/radem-hutis-nebius-agent.git
cd radem-hutis-nebius-agent
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it, then install dependencies:

```bash
pip install -r requirements.txt
```

### 3. Configure environment variables

Copy `.env.example` to `.env` and add your own Nebius Token Factory key.

```env
NEBIUS_API_KEY=your_key_here
NEBIUS_BASE_URL=https://api.tokenfactory.nebius.com/v1/
NEMOTRON_MODEL=nvidia/Nemotron-3_5-Lightning
```

Never commit `.env`.

### 4. Run the API

```bash
uvicorn api.main:app --reload
```

Health check:

```text
GET http://127.0.0.1:8000/health
```

Reasoning request:

```text
POST http://127.0.0.1:8000/v1/reason
```

Example body:

```json
{
  "readiness_context": {
    "dimensions": {
      "awareness": 72,
      "acceptance": 61,
      "capacity": 58,
      "alignment": 66,
      "sustainability": 55
    }
  },
  "goal": "Generate a concise transformation roadmap."
}
```

## Token Factory acceleration

Token Factory provides the model-access layer for rapid experimentation with NVIDIA Nemotron models through one OpenAI-compatible integration. The repository isolates model access behind `agents/nemotron_agent.py`, so model variants can be benchmarked without rewriting the HUTIS API or assessment logic.

**Important:** measured latency, throughput, cost, and final model-selection claims will be added only after live benchmark runs.

## Responsible AI

The prototype is designed for transformation readiness and decision support. It is not intended for surveillance, automated employment decisions, medical diagnosis, or other high-stakes automated determinations.

HUTIS outputs should be treated as structured decision-support information and reviewed by a human.

## License

MIT License.

## Project

**RADEM GLOBAL AI**  
Human Transformation Intelligence System  
Web: https://www.rademglobal.com  
Demo: https://ai.rademglobal.com
