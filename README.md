# Meeting Plunger

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
go run .
```

## Project Structure

```
.
├── backend/          # Python FastAPI backend
├── client/           # Golang CLI and local HTTP service
├── flake.nix         # Nix development environment
└── README.md
```

## Technology Stack

- **Backend**: Python 3.11, FastAPI, running on Kubernetes
- **Client**: Golang, CLI + HTTP server
- **Infrastructure**: Kubernetes (k8s)
- **AI Integration**: OpenAI API
- **Authentication**: Token-based auth over HTTPS
