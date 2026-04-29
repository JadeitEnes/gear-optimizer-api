import logging
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.database.models import CPU, GPU, RAM, Resolution
from app.schemas.gear_schema import CPUResponse, GPUResponse, RamResponse, ResolutionResponse
from app.repositories.hardware_repository import HardwareRepository
from typing import List

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/hardware",
    tags=["Hardware"],
)

@router.get("/cpus", response_model=List[CPUResponse])
def get_cpus(db: Session = Depends(get_db)) -> List[CPU]:
    return HardwareRepository(db).get_all_cpus()

@router.get("/gpus", response_model=List[GPUResponse])
def get_gpus(db: Session = Depends (get_db)) -> List [GPU]:
    return HardwareRepository(db).get_all_gpus()

@router.get("/rams", response_model=List[RamResponse])
def get_rams(db: Session = Depends (get_db)) -> List[RAM]:
    return HardwareRepository(db).get_all_rams()

@router.get("/resolution", response_model=List[ResolutionResponse])
def get_resolutions(db: Session = Depends (get_db)) -> List[Resolution]:
    return HardwareRepository(db).get_all_resolutions()
