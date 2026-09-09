from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.schemas.gear_schema import GearInput, GearOutput
from app.services.optimizer_service import OptimizerService
from app.repositories.hardware_repository import HardwareRepository

router = APIRouter(
    prefix="/optimizer",
    tags=["Gear Optimizer"],
)


@router.post("/analyze", response_model=GearOutput)
def analyze_gear(gear: GearInput, db: Session = Depends(get_db)) -> GearOutput:
    service = OptimizerService(HardwareRepository(db))
    return service.analyze(gear)
