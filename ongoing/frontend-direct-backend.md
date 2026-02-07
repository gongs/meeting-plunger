# Frontend Uses Backend Directly (Skip Local Service)

## Requirement

Frontend talks to backend directly; local-service is bypassed.

## Changes Made

- **Vite proxy**: `/transcribe` and `/health` now proxy to `http://localhost:8000` (backend) instead of `http://localhost:3001` (local-service)
- **sut script**: Starts only backend + frontend (removed local-service)
- **CI workflow**: Removed local-service startup, health check, and shutdown
- **Cursor rules**: Updated general.mdc and e2e-testing.mdc

## Status

Done. E2E tests pass.
