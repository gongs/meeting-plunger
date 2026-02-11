from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from openai import OpenAI
from pydantic import BaseModel

from config import OPENAI_API_KEY
from database import Base, engine, SessionLocal
from models.venue import Venue
from routers.auth import router as auth_router
from routers.venues import router as venues_router

app = FastAPI(title="Meeting Plunger API")
app.include_router(auth_router)
app.include_router(venues_router)


@app.on_event("startup")
def startup():
    """Ensure database schema exists and default venue exists."""
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        if db.query(Venue).count() == 0:
            db.add(Venue(name="默认赛场"))
            db.commit()
    finally:
        db.close()


# Initialize OpenAI client
openai_client = OpenAI(api_key=OPENAI_API_KEY)


# Testability: Mock control
class MockConfig(BaseModel):
    enabled: bool
    transcript: str = ""


mock_config = MockConfig(enabled=False)

# Configure CORS for local development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "Meeting Plunger API", "status": "running"}


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


@app.post("/transcribe")
async def transcribe(file: UploadFile = File(...)):  # noqa: B008
    """Transcribe audio file using OpenAI API."""
    # Check if mock is enabled
    if mock_config.enabled:
        return {"transcript": mock_config.transcript}

    # Read the uploaded file content
    audio_content = await file.read()

    # Create a temporary file-like object for OpenAI API
    audio_file = (file.filename, audio_content, file.content_type)

    # Call OpenAI Transcription API
    transcript = openai_client.audio.transcriptions.create(
        model="gpt-4o-mini-transcribe", file=audio_file
    )

    return {"transcript": transcript.text}


@app.post("/testability/mock")
async def set_mock(config: MockConfig):
    """Testability endpoint: Configure mocked responses."""
    global mock_config
    mock_config = config
    return {"status": "ok", "mock_enabled": mock_config.enabled}


@app.post("/testability/reset-db")
async def reset_db():
    """Testability endpoint: Reset database (drop and recreate all tables)."""
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        if db.query(Venue).count() == 0:
            db.add(Venue(name="默认赛场"))
            db.commit()
    finally:
        db.close()
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
