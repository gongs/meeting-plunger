# Unit Testing Guide

## Overview

This document describes the unit testing setup for Meeting Plunger's local-service and backend.

## Running Tests

### Backend Tests (Python/FastAPI)

```bash
# Run from project root
nix develop -c pnpm test:backend

# Run directly from backend directory
cd backend
nix develop -c pnpm test
```

### Local Service Tests (Go)

```bash
# Run from project root
nix develop -c pnpm test:local-service

# Run directly from local-service directory
cd local-service
nix develop -c make test
```

## Test Files

### Backend: `backend/tests/test_main.py`

Tests the FastAPI endpoints using FastAPI's TestClient:

- **test_root_endpoint()** - Tests the root `/` endpoint returns correct message
- **test_health_check()** - Tests the `/health` endpoint returns healthy status
- **test_cors_credentials()** - Tests CORS credentials are properly configured

**Note**: Python tests follow the convention of being in a separate `tests/` directory.

### Local Service: `local-service/handlers_test.go`

Tests the Go HTTP handlers using httptest:

- **TestHandleRoot()** - Tests the root handler returns HTML with correct content
- **TestHandleHealth()** - Tests the health handler returns JSON with healthy status

**Note**: Go tests follow the convention of being in the same directory as the code under test.

## Framework Details

### Backend (pytest)

- **Framework**: pytest with FastAPI TestClient
- **Configuration**: `pytest -v` (verbose mode)
- **Dependencies**: Already in `requirements.txt`
- **Async Support**: pytest-asyncio available for async tests

### Local Service (Go testing)

- **Framework**: Standard Go testing package
- **Test Discovery**: Files matching `*_test.go`
- **Run Command**: `go test -v ./...`
- **HTTP Testing**: Uses `net/http/httptest` for request/response testing

## Adding New Tests

### Backend (Python)

1. Create test files in `backend/tests/` with prefix `test_*.py`
2. Test functions must start with `test_`
3. Use TestClient for endpoint testing:

```python
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_my_endpoint():
    response = client.get("/my-endpoint")
    assert response.status_code == 200
```

### Local Service (Go)

1. Create test files in the same directory as the code with suffix `*_test.go`
2. Test functions must match `func TestXxx(t *testing.T)`
3. Use the same package name as the code being tested
4. Use httptest for handler testing:

```go
package main

import (
    "net/http"
    "net/http/httptest"
    "testing"
)

func TestMyHandler(t *testing.T) {
    req, _ := http.NewRequest("GET", "/my-endpoint", nil)
    rr := httptest.NewRecorder()
    handler := http.HandlerFunc(MyHandler)
    handler.ServeHTTP(rr, req)
    
    if rr.Code != http.StatusOK {
        t.Errorf("expected status 200, got %d", rr.Code)
    }
}
```

**Note**: Go convention is to place test files alongside the source code, not in a separate directory.

## Best Practices

1. **Keep tests simple** - Each test should verify one behavior
2. **Use descriptive names** - Test names should explain what they test
3. **Arrange-Act-Assert** - Structure tests in three clear sections
4. **Avoid external dependencies** - Unit tests should not require running services
5. **Run tests frequently** - Tests run fast, use them during development

## Integration with CI/CD

The unit test commands can be integrated into CI/CD pipelines:

```bash
# Run all unit tests
nix develop -c pnpm test:backend && nix develop -c pnpm test:local-service
```

## See Also

- [Quick Start Guide](QUICK_START.md)
- [E2E Testing Guide](../e2e/README.md)
- [VSCode Setup](VSCODE_SETUP.md)
