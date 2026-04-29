import logging
from enum import Enum
from app.repositories.hardware_repository import HardwareRepository
from app.schemas.gear_schema import GearInput, GearOutput
from app.enums import UsagePurpose

logger = logging.getLogger(__name__)

class UsagePurpose(str, Enum):
    GAMING = "gaming"
    VIDEO_EDITING = "video_editing"
    SOFTWARE_DEVELOPMENT = "software_development"

USAGE_ADVICE: dict[UsagePurpose, str] = {
    UsagePurpose.GAMING: "Yüksek frekanslı RAM ve güçlü GPU önceliğiniz olmalı.",
    UsagePurpose.VIDEO_EDITING: "Çok çekirdekli CPU ve 32GB+ RAM kritik önem taşıyor.",
    UsagePurpose.SOFTWARE_DEVELOPMENT: "Hızlı SSD ve 16GB+ RAM geliştirme deneyimini doğrudan etkiler.",
}

class OptimizerService:
    def __init__(self, repository: HardwareRepository) -> None:
        self.repository = repository

    def analyze(self, gear: GearInput) -> GearOutput:

        cpu = self.repository.get_cpu_by_id(gear.cpu_id)
        gpu = self.repository.get_gpu_by_id(gear.gpu_id)
        ram = self.repository.get_ram_by_id(gear.ram_id)
        resolution = self.repository.get_resolution_by_id(gear.resolution_id)

        self._validate_components(cpu, gpu, ram, resolution)

        gpu_score_adjusted = int(gpu.score / resolution.demand_multiplier)

        total_score = int((cpu.score + gpu_score_adjusted + ram.score ) / 3)
        level = self.calculate_level(total_score)
        advice = USAGE_ADVICE.get(
            gear.usage_purpose,
            " Kullanım amacınızı giriniz."
        )

        logger.info(
            f"Analysis complete - score={total_score}, level={level},"
            f"cpu={cpu.model}, gpu={gpu.model}, resolution={resolution.name}"
        )

        return GearOutput(
            score=total_score,
            level=level,
            advice=advice,
            detail={
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
        )
    def _validate_component(self, cpu, gpu, ram, resolution) -> None:
        missing = []
        if not cpu: missing.append("CPU")
        if not gpu: missing.append("GPU")
        if not ram: missing.append("RAM")
        if not resolution: missing.append("Resolution")
        if missing:
            logger.warning(f"Invalid component IDs: {missing}")
            raise ValueError(f"Geçersiz donanım ID'si: {', '.join(missing)}")


    def _calculate_level(self, score: int) -> str:
        if score >= 80: return "Profesyonel"
        if score >= 60: return "Üst Seviye"
        if score >= 40: return "Orta Seviye"
        return "Giriş Seviye"





   
    

    
    
    
    

   