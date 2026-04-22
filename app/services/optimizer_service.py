from sqlalchemy.orm import Session
from app.database.models import CPU, GPU, RAM, Resolution
from app.schemas.gear_schema import GearInput, GearOutput

USAGE_ADVICE = {
    "gaming": "Yüksek frekanslı RAM ve güçlü GPU önceliğiniz olmalı.",
    "video_editing": "Çok çekirdekli CPU ve 32GB+ RAM kritik önem taşıyor.",
    "software_development": "Hızlı SSD ve 16GB+ RAM geliştirme deneyimini doğrudan etkiler.",
}

def calculate_gear_score(gear: GearInput, db: Session) -> GearOutput:
    cpu = db.query(CPU).filter(CPU.id == gear.cpu_id).first()
    gpu = db.query(GPU).filter(GPU.id == gear.gpu_id).first()
    ram = db.query(RAM).filter(RAM.id == gear.ram_id).first()
    resolution = db.query(Resolution).filter(Resolution.id == gear.resolution_id).first()

    if not all([cpu, gpu, ram, resolution]):
        raise ValueError("Geçersiz ID.")
    
    gpu_score_adjusted = int(gpu.score / resolution.demand_multiplier)

    total_score = int((cpu.score + gpu_score_adjusted + ram.score ) / 3)

    
    if total_score >= 80:
        level = "Profesyonel"
    elif total_score >= 60:
        level = "Üst Seviye"
    elif total_score >= 40:
        level = "Orta Seviye"
    else:
        level = "Giriş Seviye"    
    advice = USAGE_ADVICE.get(
        gear.usage_purpose.lower(),
        "Sistemin kullanım amacını giriniz."
    )
    detail = {
        "cpu": f"{cpu.brand} {cpu.model}",
        "cpu_score": cpu.score,
        "gpu": f"{gpu.brand} {gpu.model}",
        "gpu_score_raw": gpu.score,
        "gpu_score_adjusted": gpu_score_adjusted,
        "ram": f"{ram.capacity_gb}GB {ram.speed_mhz}MHz",
        "ram_score": ram.score,
        "resolution": resolution.name,
        "demand_multiplier": resolution.demand_multiplier,
    }

    return GearOutput(
        score=total_score,
        level=level,
        advice=advice,
        detail=detail,
    )