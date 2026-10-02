# Live Nemotron Benchmark

This repository includes a repeatable benchmark script for the HUTIS reasoning workload.

## Candidate model

The current default candidate is:

```text
nvidia/Nemotron-3_5-Lightning
```

Nebius currently lists Nemotron 3.5 Lightning as a public Token Factory model intended for efficient agentic reasoning, coding, tool use, and long-context workflows.

## Run

Set `NEBIUS_API_KEY` in your local environment, then:

```bash
python scripts/benchmark_nemotron.py
```

The script records:

- model ID
- request latency
- prompt tokens
- completion tokens
- total tokens
- completion tokens per second
- model response

The latest result is written to:

```text
benchmarks/latest.json
```

## Evaluation protocol

For the hackathon submission, compare at least three repeated runs using the same HUTIS prompt before making latency or throughput claims.

Recommended comparison set:

1. Nemotron 3.5 Lightning — efficiency-first candidate.
2. Nemotron 3 Super 120B — quality/cost balance candidate.
3. Nemotron 3 Nano 30B — cost-efficient baseline.

Use identical prompts and record model availability, latency, token usage, response quality, and any failures.

## Evidence rule

Do not state measured performance in README or submission materials until the value is produced by an actual Token Factory run and saved here.
