from contextlib import asynccontextmanager
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config import settings
from database.db import init_db
from api.routes import router
from camera.video_processor import VideoProcessor
from alerts.voice_alert import VoiceAlertService

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: initialize database tables and seed defaults
    init_db()
    yield
    # Shutdown: release camera and voice service
    processor = VideoProcessor.get_instance()
    processor.stop_monitoring()
    voice = VoiceAlertService.get_instance()
    voice.shutdown()

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Edge-Enabled Privacy-Preserving System for Construction Workspace Management",
    lifespan=lifespan
)

# Configure CORS for local React dashboard
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)

@app.get("/")
def root():
    return {
        "status": "online",
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "docs_url": "/docs",
        "privacy_mode": "EDGE_LOCAL_FIRST"
    }

if __name__ == "__main__":
    uvicorn.run("main:app", host=settings.HOST, port=settings.PORT, reload=False)
