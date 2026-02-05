# API Type Sharing

This document describes how API definitions are shared between the Go client and TypeScript frontend.

## Overview

The Meeting Plunger project uses OpenAPI/Swagger to maintain a single source of truth for API types. The Go client generates an OpenAPI specification from code annotations, which can then be used to generate TypeScript types for the frontend.

## Architecture

```
Go Client (handlers.go)
  ↓ swag annotations
  ↓ swag init
OpenAPI Spec (client/generated/openapi.json)
  ↓ openapi-typescript (future)
TypeScript Types (frontend/src/types/api.ts)
```

## Current Setup

### Go Client → OpenAPI

The Go client uses [swaggo/swag](https://github.com/swaggo/swag) to generate OpenAPI specs from code annotations.

**Location:** `client/generated/openapi.json`

**Generate:**
```bash
nix develop -c pnpm generate:openapi
```

**Validate (CI check):**
```bash
nix develop -c pnpm validate:openapi
```

**Example annotations in `client/handlers.go`:**
```go
// HealthResponse represents the health check response
type HealthResponse struct {
    Status string `json:"status" example:"healthy"`
}

// HandleHealth serves the health check endpoint
// @Summary Health check
// @Description Returns the health status of the client service
// @Tags health
// @Produce json
// @Success 200 {object} HealthResponse
// @Router /health [get]
func HandleHealth(w http.ResponseWriter, r *http.Request) {
    // ...
}
```

### OpenAPI → TypeScript (Future)

To generate TypeScript types from the OpenAPI spec, you can use [openapi-typescript](https://github.com/drwpow/openapi-typescript):

```bash
# Install
pnpm add -D openapi-typescript

# Generate types
npx openapi-typescript client/generated/openapi.json -o frontend/src/types/api.ts
```

**Example generated types:**
```typescript
export interface HealthResponse {
  status?: string;
}

export interface TranscriptResponse {
  transcript?: string;
}
```

## Workflow

### When Adding/Modifying API Endpoints

1. **Update Go handlers** with swag annotations
2. **Regenerate OpenAPI spec:**
   ```bash
   nix develop -c pnpm generate:openapi
   ```
3. **Validate it's up to date** (optional, CI will check):
   ```bash
   nix develop -c pnpm validate:openapi
   ```
4. **Generate TypeScript types** (when set up):
   ```bash
   pnpm generate:types:frontend
   ```
5. **Commit both** the Go code and generated files

**Note:** CI will automatically validate that the generated OpenAPI spec matches the code. If you forget to regenerate after modifying the API, the CI build will fail with a helpful diff.

### When Using API Types

**Frontend (TypeScript):**
```typescript
import type { TranscriptResponse } from '@/types/api';

const response = await fetch('/upload', {
  method: 'POST',
  body: formData,
});

const data: TranscriptResponse = await response.json();
console.log(data.transcript);
```

**Client (Go):**
```go
type TranscriptResponse struct {
    Transcript string `json:"transcript" example:"Hello, how are you?"`
}

// Use directly in handlers
```

## Benefits

1. **Type Safety:** Catch API contract violations at compile time
2. **Single Source of Truth:** Go code is the authoritative API definition
3. **Documentation:** OpenAPI spec serves as API documentation
4. **Tooling:** Can generate clients, mocks, validators, etc.

## File Locations

| File | Description | Committed? |
|------|-------------|------------|
| `client/handlers.go` | Go handlers with swag annotations | ✅ Yes |
| `client/generated/openapi.json` | Generated OpenAPI spec | ✅ Yes |
| `frontend/src/types/api.ts` | Generated TypeScript types (future) | ✅ Yes |

## References

- [swaggo/swag](https://github.com/swaggo/swag) - Swagger generator for Go
- [openapi-typescript](https://github.com/drwpow/openapi-typescript) - Generate TypeScript from OpenAPI
- [OpenAPI Specification](https://swagger.io/specification/) - API standard
