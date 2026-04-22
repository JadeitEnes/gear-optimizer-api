from fastapi import APIRouter, Depends,  HTTPException
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.schemas.gear_schema import GearInput, GearOutput
from app.services.optimizer_service import calculate_gear_score

router = APIRouter(
    prefix ="/optimizer",
    tags = ["Gear Optimizer"],
)
@router.post("/analyze", response_model=GearOutput)
def analyze_gear(gear: GearInput, db: Session = Depends(get_db)):
    try:
        return calculate_gear_score(gear)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    