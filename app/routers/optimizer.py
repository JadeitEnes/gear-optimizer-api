import logging
from fastapi import APIRouter, Depends,  HTTPException
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.schemas.gear_schema import GearInput, GearOutput
from app.services.optimizer_service import OptimizerService
from app.repositories.hardware_repository import HardwareRepository

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix ="/optimizer",
    tags = ["Gear Optimizer"],
)

@router.post("/analyze", response_model=GearOutput)
def analyze_gear(gear: GearInput, db: Session = Depends(get_db)) -> GearOutput:

    try:
        repository = HardwareRepository(db)
        service = OptimizerService(repository)
        return service.analyze(gear)

    
    except ValueError as e:
        logger.error(f"Analysis failed: {e}")
        raise HTTPException(status_code=404, detail=str(e))
    