import logging
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from app.routers import optimizer, hardware
from app.database.database import engine
from app.database.models import Base
from app.database.seed import seed_data
from contextlib import asynccontextmanager
from app.config import get_settings

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s — %(name)s — %(levelname)s — %(message)s"
)

logger = logging.getLogger(__name__)
settings = get_settings()

Base.metadata.create_all(bind=engine)

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info(f"Starting {settings.app_name} v{settings.app_version}")
    seed_data()
    logger.info("Application ready")
    yield

app = FastAPI(
    title = settings.app_name,
    description = "Donanım ve performans optimizasyon API'si",
    version = settings.app_version,
    lifespan = lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(optimizer.router)
app.include_router(hardware.router)
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/ui")
def serve_ui() -> FileResponse:
    return FileResponse("static/index.html")

@app.get("/")
def root() -> dict:
    return {
        "app": settings.app_name,
        "version": settings.app_version,
        "status": "running"
    }

