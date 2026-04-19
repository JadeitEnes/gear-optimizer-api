from fastapi import APIRouter
from app.schemas.gear_schema import GearInput, GearOutput
from app.services.optimizer_service import calculate_gear_score

router = APIRouter(
    prefix ="/optimizer",
    tags = ["Gear Optimizer"],
)
@router.post("/analyze", response_model=GearOutput)
def analyze_gear(gear: GearInput):
    return calculate_gear_score(gear)