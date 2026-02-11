import os
from pathlib import Path

from dotenv import load_dotenv

# Load .env from backend directory (so it works regardless of cwd when running uvicorn)
_backend_dir = Path(__file__).resolve().parent
load_dotenv(_backend_dir / ".env")

# OpenAI Configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Database: default to backend/meeting_plunger.db so path is stable regardless of cwd
_default_db = f"sqlite:///{_backend_dir / 'meeting_plunger.db'}"
DATABASE_URL = os.getenv("DATABASE_URL", _default_db)

# Note: OPENAI_API_KEY validation is deferred to runtime when actually needed.
# This allows importing the module (e.g., for OpenAPI schema generation) without requiring the key.
