#!/usr/bin/env bash
set -euo pipefail

# Script to generate OpenAPI spec from Go client using swaggo/swag
# The generated openapi.json will be placed in client/generated/

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
CLIENT_DIR="$PROJECT_ROOT/client"
GENERATED_DIR="$CLIENT_DIR/generated"

echo "🔄 Generating OpenAPI spec for Go client..."
echo "   Client dir: $CLIENT_DIR"
echo "   Output dir: $GENERATED_DIR"
echo ""

# Ensure generated directory exists
mkdir -p "$GENERATED_DIR"

# Run swag init from the client directory
# --parseDependency: parse Go files in dependencies
# --parseInternal: parse Go files in internal packages
# --parseDepth: dependency parse depth (default is 100)
# --output: output directory for docs (we'll move the file afterwards)
cd "$CLIENT_DIR"

echo "Running swag init..."
nix develop -c sh -c "\$(go env GOPATH)/bin/swag init \
  --parseDependency \
  --parseInternal \
  --output \"$GENERATED_DIR\""

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
echo "   File: client/generated/openapi.json"
echo ""
echo "To view the spec:"
echo "  cat client/generated/openapi.json | jq"
