# Architecture

## Hackathon architecture

```text
HUTIS Assessment
      |
      v
Readiness Analysis
      |
      v
Context Builder
      |
      v
FastAPI /v1/reason
      |
      v
Nebius Token Factory
      |
      v
NVIDIA Nemotron
      |
      v
Adaptive Roadmap
      |
      v
T0 → T1 → T2 Measurement
```

## Design principles

- Keep proprietary HUTIS scoring logic separate from the public inference adapter.
- Send only the minimum context required for reasoning.
- Keep provider credentials outside source control.
- Make the model ID configurable so Nemotron variants can be evaluated without code changes.
- Treat generated recommendations as human-reviewed decision support.
- Record benchmark evidence before making performance claims.

## Current scope

This public repository demonstrates the hackathon-facing inference integration and API contract. It does not expose proprietary RADEM methodology internals or production datasets.
