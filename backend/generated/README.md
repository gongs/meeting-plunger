# Backend Generated Files

This directory contains generated files from the FastAPI backend.

## Files

- `openapi.json` - OpenAPI 3.0 specification fetched from FastAPI's `/openapi.json` endpoint

## Generation

Generated automatically by:
```bash
nix develop -c pnpm generate:api
```

Or specifically:
```bash
nix develop -c scripts/generate-backend-openapi.sh
```

## Why Commit?

These files are committed to ensure:
- Consistent API contracts across development, CI, and production
- Code review visibility of API changes
- Downstream code generation (Go client for local-service)
