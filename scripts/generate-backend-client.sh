#!/usr/bin/env bash
set -euo pipefail

# Script to generate Go client code from backend OpenAPI spec using oapi-codegen
# The generated client will be placed in local-service/generated/backend_client/

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
BACKEND_DIR="$PROJECT_ROOT/backend"
LOCAL_SERVICE_DIR="$PROJECT_ROOT/local-service"
OPENAPI_SPEC="$BACKEND_DIR/generated/openapi.json"
OUTPUT_DIR="$LOCAL_SERVICE_DIR/generated/backend_client"
OUTPUT_FILE="$OUTPUT_DIR/client.go"

echo "🔄 Generating Go client from backend OpenAPI spec..."
echo "   Input spec: $OPENAPI_SPEC"
echo "   Output dir: $OUTPUT_DIR"
echo ""

# Check if OpenAPI spec exists
if [ ! -f "$OPENAPI_SPEC" ]; then
  echo "❌ Error: Backend OpenAPI spec not found at $OPENAPI_SPEC"
  echo ""
  echo "Please generate the backend OpenAPI spec first:"
  echo "  nix develop -c pnpm generate:api"
  exit 1
fi

# Ensure output directory exists
mkdir -p "$OUTPUT_DIR"

# Run oapi-codegen to generate Go client
echo "Running oapi-codegen..."

# Check if running in CI or if nix is not available
if [ "${CI:-false}" = "true" ] || ! command -v nix > /dev/null 2>&1; then
  # Running in CI or without Nix - oapi-codegen should be in PATH
  oapi-codegen -package backendclient -generate types,client -o "$OUTPUT_FILE" "$OPENAPI_SPEC"
else
  # Running locally with Nix
  nix develop -c oapi-codegen -package backendclient -generate types,client -o "$OUTPUT_FILE" "$OPENAPI_SPEC"
fi

if [ -f "$OUTPUT_FILE" ]; then
  echo "✅ Generated: $OUTPUT_FILE"
else
  echo "❌ Error: Failed to generate Go client"
  exit 1
fi

echo ""
echo "✅ Go client generation complete!"
echo "   File: local-service/generated/backend_client/client.go"
echo ""
echo "Usage in Go code:"
echo "  import \"meeting-plunger/local-service/generated/backendclient\""
echo "  client, _ := backendclient.NewClient(\"http://localhost:8000\")"
