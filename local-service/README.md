# Local Service (Golang)

Golang local HTTP service for Meeting Plunger. The local-service bridges communication between the frontend (Vue.js) and backend (Python), processing audio files locally using the user's machine resources.

## Development

The local-service uses `air` for live reload during development. Changes to `.go` files automatically trigger a rebuild.

### Start with Auto-Reload

From the project root:
```bash
nix develop -c pnpm sut
```

Or run the local-service alone:
```bash
nix develop -c pnpm sut:local-service
```

Or directly:
```bash
cd local-service
nix develop -c air
```

### Build Binary

```bash
cd local-service
nix develop -c go build -o local-service .
./local-service serve
```

## Configuration

- **`.air.toml`** - Air live reload configuration
  - Watches `.go` files
  - Rebuilds to `tmp/main`
  - Runs with `serve` argument
  - Cleans up on exit

## How It Works

When you change a `.go` file:
1. `air` detects the change
2. Rebuilds the binary to `tmp/main`
3. Kills the old process
4. Starts the new binary with `serve` argument
5. Server is ready in ~1-2 seconds

## Architecture

**Request Flow:**
```
Frontend (Vue :3000) → Local Service (Go :3001) → Backend (Python :8000) → OpenAI API
```

The local-service runs on port 3001 and:
- Receives requests from the frontend
- Handles file uploads and processes audio locally
- Communicates with the backend API for AI services
- Returns transcription results

## API Documentation

### OpenAPI Specification

The local-service API is documented using OpenAPI/Swagger. The specification is automatically generated from code annotations using [swaggo/swag](https://github.com/swaggo/swag).

**Generated spec:** `local-service/generated/openapi.json`

#### Regenerate OpenAPI Spec

After modifying API endpoints or their annotations:

```bash
# From project root
nix develop -c pnpm generate:openapi

# Or run the script directly
./scripts/generate-local-service-openapi.sh
```

#### Validate OpenAPI Spec

Check if the generated spec is up to date (used in CI):

```bash
# From project root
nix develop -c pnpm validate:api

# Or run the script directly
./scripts/validate-api-generation.sh
```

The validation will fail with a diff if the generated file doesn't match the code. This ensures the OpenAPI spec is always kept in sync with the API implementation.

The generated `openapi.json` file is committed to the repository and is used to:
- Generate TypeScript client and SDK for the frontend (automatically via `pnpm generate:api`)
- View in Swagger UI or other OpenAPI tools
- Generate API clients for other languages if needed

**Frontend integration:**
The OpenAPI spec is automatically converted to TypeScript client code including:
- Type-safe service classes (`TranscriptionService`, `HealthService`)
- Type definitions for all requests and responses
- Error handling with `ApiError`
- No need for manual fetch/response.json() calls

### Endpoints

- **GET /health** - Health check endpoint
- **POST /upload** - Upload audio file for transcription (returns hardcoded response for now)

## Commands

```bash
# Run with live reload (recommended for development)
air

# Run directly (no reload)
go run . serve

# Build binary
go build -o local-service .

# Run binary
./local-service serve
```

## CLI Usage

```bash
# Show help
go run .

# Start HTTP server
go run . serve
```
