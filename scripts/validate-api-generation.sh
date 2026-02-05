#!/usr/bin/env bash
set -euo pipefail

# Script to validate that the generated OpenAPI spec is up to date
# Used in CI to ensure developers regenerate the spec after changing API code

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
CLIENT_DIR="$PROJECT_ROOT/client"
GENERATED_FILE="$CLIENT_DIR/generated/openapi.json"

echo "🔍 Validating OpenAPI spec is up to date..."
echo ""

# Check if the generated file exists
if [ ! -f "$GENERATED_FILE" ]; then
  echo "❌ Error: Generated OpenAPI spec not found at $GENERATED_FILE"
  echo ""
  echo "Please run: nix develop -c pnpm generate:openapi"
  exit 1
fi

# Create a temporary directory for the newly generated file
TEMP_DIR=$(mktemp -d)
trap "rm -rf $TEMP_DIR" EXIT

# Copy the current generated file to temp for comparison
cp "$GENERATED_FILE" "$TEMP_DIR/openapi.json.old"

echo "Regenerating OpenAPI spec..."
"$SCRIPT_DIR/generate-client-openapi.sh" > /dev/null 2>&1

# Compare the files
if ! diff -q "$TEMP_DIR/openapi.json.old" "$GENERATED_FILE" > /dev/null 2>&1; then
  echo ""
  echo "❌ ERROR: Generated OpenAPI spec is out of date!"
  echo ""
  echo "The committed openapi.json differs from the generated version."
  echo "This usually means the Go API code was modified but the spec wasn't regenerated."
  echo ""
  echo "📋 Differences:"
  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
  
  # Show colorful diff if available, otherwise plain diff
  if command -v colordiff > /dev/null 2>&1; then
    diff -u "$TEMP_DIR/openapi.json.old" "$GENERATED_FILE" | colordiff || true
  else
    diff -u "$TEMP_DIR/openapi.json.old" "$GENERATED_FILE" || true
  fi
  
  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
  echo ""
  echo "🔧 To fix this:"
  echo "   1. Run: nix develop -c pnpm generate:openapi"
  echo "   2. Commit the updated client/generated/openapi.json"
  echo ""
  
  # Restore the old file so the working directory is not modified
  cp "$TEMP_DIR/openapi.json.old" "$GENERATED_FILE"
  
  exit 1
fi

echo "✅ OpenAPI spec is up to date!"
echo ""
exit 0
