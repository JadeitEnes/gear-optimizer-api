from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from app.routers import optimizer, hardware
from app.database.database import engine
from app.database.models import Base
from app.database.seed import seed_data
from contextlib import asynccontextmanager

Base.metadata.create_all(bind=engine)

@asynccontextmanager
async def lifespan(app: FastAPI):
    seed_data()
    yield

app = FastAPI(
    title = "GearOptimizer API",
    description = "Donanım ve performans optimizasyon API'si",
    version = "2.0.0",
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

@app.get("/")
def root():
    return {"message":"GearOptimizer API v2.0 is running"}

