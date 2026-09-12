import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from app.routers import optimizer, hardware
from app.database.seed import seed_data
from app.exceptions import ComponentNotFoundError, SharedBuildNotFoundError
from app.config import get_settings

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s — %(name)s — %(levelname)s — %(message)s"
)

logger = logging.getLogger(__name__)
settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info(f"Starting {settings.app_name} v{settings.app_version}")
    seed_data()
    logger.info("Application ready")
    yield


app = FastAPI(
    title=settings.app_name,
    description="Donanım ve performans optimizasyon API'si",
    version=settings.app_version,
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type"],
)


@app.exception_handler(ComponentNotFoundError)
async def component_not_found_handler(request: Request, exc: ComponentNotFoundError) -> JSONResponse:
    logger.warning(f"Component not found: {exc.missing}")
    return JSONResponse(status_code=404, content={"detail": str(exc)})


@app.exception_handler(SharedBuildNotFoundError)
async def shared_build_not_found_handler(request: Request, exc: SharedBuildNotFoundError) -> JSONResponse:
    logger.warning(f"Shared build not found: {exc.slug}")
    return JSONResponse(status_code=404, content={"detail": str(exc)})


app.include_router(optimizer.router)
app.include_router(hardware.router)
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/ui", include_in_schema=False)
def serve_ui() -> FileResponse:
    return FileResponse("static/index.html")


@app.get("/health", tags=["System"])
def health() -> dict:
    return {"status": "ok"}


@app.get("/")
def root() -> dict:
    return {
        "app": settings.app_name,
        "version": settings.app_version,
        "status": "running"
    }
