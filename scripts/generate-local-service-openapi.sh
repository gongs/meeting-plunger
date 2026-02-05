#!/usr/bin/env bash
set -euo pipefail

# Script to generate OpenAPI spec from Go local-service using swaggo/swag
# The generated openapi.json will be placed in local-service/generated/

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
LOCAL_SERVICE_DIR="$PROJECT_ROOT/local-service"
GENERATED_DIR="$LOCAL_SERVICE_DIR/generated"

echo "🔄 Generating OpenAPI spec for Go local-service..."
echo "   Local service dir: $LOCAL_SERVICE_DIR"
echo "   Output dir: $GENERATED_DIR"
echo ""

# Ensure generated directory exists
mkdir -p "$GENERATED_DIR"

# Run swag init from the local-service directory
# --parseDependency: parse Go files in dependencies
# --parseInternal: parse Go files in internal packages
# --parseDepth: dependency parse depth (default is 100)
# --output: output directory for docs (we'll move the file afterwards)
cd "$LOCAL_SERVICE_DIR"

echo "Running swag init..."

# Check if running in CI or if nix is not available
if [ "${CI:-false}" = "true" ] || ! command -v nix > /dev/null 2>&1; then
  # Running in CI or without Nix - swag should be in PATH
  SWAG_CMD="swag"
  # Try GOPATH/bin if swag is not in PATH
  if ! command -v swag > /dev/null 2>&1; then
    SWAG_CMD="$(go env GOPATH)/bin/swag"
  fi
  
  $SWAG_CMD init \
    --parseDependency \
    --parseInternal \
    --output "$GENERATED_DIR"
else
  # Running locally with Nix
  nix develop -c sh -c "\$(go env GOPATH)/bin/swag init \
    --parseDependency \
    --parseInternal \
    --output \"$GENERATED_DIR\""
fi

# Keep only the swagger.json and rename it to openapi.json
if [ -f "$GENERATED_DIR/swagger.json" ]; then
  mv "$GENERATED_DIR/swagger.json" "$GENERATED_DIR/openapi.json"
  echo "✅ Generated: $GENERATED_DIR/openapi.json"
else
  echo "❌ Error: swagger.json was not generated"
  exit 1
fi

# Clean up other generated files (docs.go, swagger.yaml)
# We only want to commit the openapi.json
rm -f "$GENERATED_DIR/docs.go"
rm -f "$GENERATED_DIR/swagger.yaml"

echo ""
echo "✅ OpenAPI generation complete!"
echo "   File: local-service/generated/openapi.json"
echo ""
echo "To view the spec:"
echo "  cat local-service/generated/openapi.json | jq"
