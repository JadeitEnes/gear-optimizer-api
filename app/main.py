from fastapi import FastAPI
from app.routers import optimizer
app = FastAPI (
    title = "GearOptimizer API",
    description = "Donanım ve performans optimizasyon API",
    version = "1.0.0"
)
app.include_router(optimizer.router)

@app.get("/")
def root():
    return {"message":"GearOptimizer API is running"}

