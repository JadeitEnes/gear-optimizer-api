from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.database.models import CPU, GPU, RAM, Resolution
from app.schemas.gear_schema import CPUResponse, GPUResponse, RamResponse, ResolutionResponse
from typing import List

router = APIRouter(
    prefix="/hardware",
    tags=["Hardware"],
)

@router.get("/cpus", response_model=List[CPUResponse])
def get_cpus(db: Session = Depends(get_db)):
    return db.query(CPU).all()

@router.get("/gpus", response_model=List[GPUResponse])
def get_gpus(db: Session = Depends (get_db)):
    return db.query(GPU).all()

@router.get("/rams", response_model=List[RamResponse])
def get_rams(db: Session = Depends (get_db)):
    return db.query(RAM).all()

@router.get("/resolution", response_model=List[ResolutionResponse])
def get_resolutions(db: Session = Depends (get_db)):
    return db.query(Resolution).all()
