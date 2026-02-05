# Backend Client (Go)

This directory contains Go client code generated from the FastAPI backend's OpenAPI specification.

## Files

- `client.go` - Type-safe Go client for calling backend endpoints

## Generation

Generated automatically by:
```bash
nix develop -c pnpm generate:api
```

Or specifically:
```bash
nix develop -c scripts/generate-backend-client.sh
```

## Usage

```go
import "meeting-plunger/local-service/generated/backendclient"

// Create client
client, err := backendclient.NewClient("http://localhost:8000")
if err != nil {
    log.Fatal(err)
}

// Use type-safe API calls
resp, err := client.PostTranscribe(ctx, file)
```

## Toolchain

Uses [oapi-codegen](https://github.com/deepmap/oapi-codegen) to generate Go client from OpenAPI 3.0 spec.
