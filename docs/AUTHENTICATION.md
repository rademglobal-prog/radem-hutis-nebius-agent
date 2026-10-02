# Authentication and Credential Handling

## Components

1. **Client** — sends a HUTIS readiness context to the local FastAPI endpoint.
2. **FastAPI layer** — validates the request schema and forwards only the required reasoning context.
3. **Nemotron adapter** — creates the OpenAI-compatible Nebius client.
4. **Nebius Token Factory** — authenticates the server-side API request.
5. **NVIDIA Nemotron model** — returns the reasoning output.

## Request flow

```text
User / Demo
   |
   | POST /v1/reason
   v
FastAPI
   |
   | validated readiness context
   v
NemotronAgent
   |
   | HTTPS request
   | Authorization credential from NEBIUS_API_KEY
   v
Nebius Token Factory
   |
   v
NVIDIA Nemotron
   |
   v
Reasoning result
   |
   v
FastAPI response
```

## Credentials

The only external-service credential required by the current integration is the Nebius API key.

`NEBIUS_API_KEY` is loaded from the runtime environment. The source code does not contain a default secret or fallback credential.

The local `.env` file is ignored by Git. Only `.env.example`, which contains placeholders, is committed.

## Tokens

This prototype does not mint its own login JWTs or refresh tokens.

The Nebius credential is handled server-side by the OpenAI-compatible SDK when it creates the outbound inference request. It is not returned to the browser or included in the API response.

## Logging

Application code must not log:
- API keys
- Authorization headers
- complete environment-variable dumps
- secrets embedded in exception messages

## Production hardening

For production deployment, add an application-level authentication layer in front of the public HUTIS API, use a managed secret store, restrict CORS, rate-limit requests, and rotate provider keys according to the deployment policy.
