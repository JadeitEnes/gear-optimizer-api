from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.schemas.gear_schema import GearInput, GearOutput, UpgradeAdvice
from app.services.optimizer_service import OptimizerService
from app.services.upgrade_advisor_service import UpgradeAdvisorService
from app.repositories.hardware_repository import HardwareRepository

router = APIRouter(
    prefix="/optimizer",
    tags=["Gear Optimizer"],
)


@router.post("/analyze", response_model=GearOutput)
def analyze_gear(gear: GearInput, db: Session = Depends(get_db)) -> GearOutput:
    service = OptimizerService(HardwareRepository(db))
    return service.analyze(gear)


@router.post("/upgrade-advice", response_model=UpgradeAdvice)
def upgrade_advice(gear: GearInput, db: Session = Depends(get_db)) -> UpgradeAdvice:
    repository = HardwareRepository(db)
    optimizer = OptimizerService(repository)
    advisor = UpgradeAdvisorService(repository, optimizer)
    return advisor.advise(gear)
