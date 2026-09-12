from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.exceptions import SharedBuildNotFoundError
from app.schemas.gear_schema import GearInput, GearOutput, UpgradeAdvice, ShareResponse
from app.services.optimizer_service import OptimizerService
from app.services.upgrade_advisor_service import UpgradeAdvisorService
from app.services.shared_build_service import SharedBuildService
from app.repositories.hardware_repository import HardwareRepository
from app.repositories.shared_build_repository import SharedBuildRepository

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


@router.post("/share", response_model=ShareResponse)
def create_share(gear: GearInput, db: Session = Depends(get_db)) -> ShareResponse:
    optimizer = OptimizerService(HardwareRepository(db))
    service = SharedBuildService(SharedBuildRepository(db), optimizer)
    build = service.create_share(gear)
    return ShareResponse(slug=build.slug)


@router.get("/share/{slug}", response_model=GearInput)
def get_shared_build(slug: str, db: Session = Depends(get_db)) -> GearInput:
    build = SharedBuildRepository(db).get_by_slug(slug)
    if build is None:
        raise SharedBuildNotFoundError(slug)

    return GearInput(
        cpu_id=build.cpu_id,
        gpu_id=build.gpu_id,
        ram_id=build.ram_id,
        resolution_id=build.resolution_id,
        usage_purpose=build.usage_purpose,
    )
