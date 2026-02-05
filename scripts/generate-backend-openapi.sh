#!/usr/bin/env bash
set -euo pipefail

# Script to generate OpenAPI spec from FastAPI backend
# The backend must be running on http://localhost:8000
# The generated openapi.json will be placed in backend/generated/

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
BACKEND_DIR="$PROJECT_ROOT/backend"
GENERATED_DIR="$BACKEND_DIR/generated"

echo "🔄 Fetching OpenAPI spec from FastAPI backend..."
echo "   Backend URL: http://localhost:8000"
echo "   Output dir: $GENERATED_DIR"
echo ""

# Ensure generated directory exists
mkdir -p "$GENERATED_DIR"

# Check if backend is running
if ! curl -s http://localhost:8000/health > /dev/null 2>&1; then
  echo "❌ Error: Backend is not running on http://localhost:8000"
  echo ""
  echo "Please start the backend first:"
  echo "  nix develop -c pnpm sut:backend"
  echo ""
  echo "Or start all services:"
  echo "  nix develop -c pnpm sut"
  exit 1
fi

# Fetch the OpenAPI spec from FastAPI
echo "Fetching OpenAPI spec from /openapi.json..."
if curl -s http://localhost:8000/openapi.json -o "$GENERATED_DIR/openapi.json"; then
  echo "✅ Generated: $GENERATED_DIR/openapi.json"
else
  echo "❌ Error: Failed to fetch OpenAPI spec"
  exit 1
fi

echo ""
echo "✅ Backend OpenAPI generation complete!"
echo "   File: backend/generated/openapi.json"
echo ""
echo "To view the spec:"
echo "  cat backend/generated/openapi.json | jq"
