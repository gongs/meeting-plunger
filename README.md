# Meeting Plunger

Meeting Plunger exists to turn messy meeting audio into usable, trustworthy meeting minutes with minimal human effort.

A monorepo project with:
- **Backend**: Python FastAPI server (deployed on k8s)
- **Client**: Golang CLI with local HTTP service for browser interface

## Architecture

```
User's Computer                    Server
┌─────────────────┐               ┌──────────────┐
│ Browser         │               │ Backend      │
│                 │               │ (Python)     │──> OpenAI API
│ Client (Golang) │─── HTTPS ────>│              │
│ CLI & HTTP      │  auth token   │ k8s          │
│ DB              │               └──────────────┘
└─────────────────┘
```

## Development Setup

### Prerequisites

- [Nix](https://nixos.org/download.html) with flakes enabled
- (Optional) [direnv](https://direnv.net/) for automatic environment loading

### Getting Started

1. Enter the development environment:

```bash
nix develop
```

Or if using direnv:
```bash
direnv allow
```

2. Start the backend:

```bash
cd backend
uvicorn main:app --reload
```

3. Start the client (in another terminal):

```bash
cd client
go run . serve
```

4. Run E2E tests (in another terminal):

```bash
cd e2e
pnpm install  # First time only
pnpm test
```

## Project Structure

```
.
├── backend/          # Python FastAPI backend
├── client/           # Golang CLI and local HTTP service
├── e2e/              # Playwright + Gherkin e2e tests
├── flake.nix         # Nix development environment
└── README.md
```

## Technology Stack

- **Backend**: Python 3.11, FastAPI, running on Kubernetes
- **Client**: Golang, CLI + HTTP server
- **E2E Testing**: Playwright + Cucumber (Gherkin), managed with pnpm
- **Infrastructure**: Kubernetes (k8s)
- **AI Integration**: OpenAI API
- **Authentication**: Token-based auth over HTTPS

## Testing

### E2E Tests

The project uses Playwright with Cucumber (Gherkin syntax) for end-to-end testing.

See [e2e/README.md](e2e/README.md) for detailed testing instructions.

**Quick start:**

```bash
# In separate terminals
cd backend && uvicorn main:app --reload
cd client && go run . serve

# Run tests
cd e2e && pnpm test
```
