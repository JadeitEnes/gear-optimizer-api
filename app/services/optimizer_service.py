import logging
from app.repositories.hardware_repository import HardwareRepository
from app.schemas.gear_schema import GearInput, GearOutput
from app.enums import UsagePurpose

logger = logging.getLogger(__name__)

WEIGHTS: dict[UsagePurpose, dict[str, float]] = {
    UsagePurpose.GAMING_GPU_INTENSIVE: {"cpu": 0.20, "gpu": 0.60, "ram": 0.20},
    UsagePurpose.GAMING_CPU_INTENSIVE: {"cpu": 0.55, "gpu": 0.25, "ram": 0.20},
    UsagePurpose.GAMING_BALANCED: {"cpu": 0.35, "gpu": 0.45, "ram": 0.20},
    UsagePurpose.VIDEO_EDITING: {"cpu": 0.30, "gpu": 0.50, "ram": 0.20},
    UsagePurpose.SOFTWARE_DEVELOPMENT: {"cpu": 0.50, "gpu": 0.10, "ram": 0.40},
}

USAGE_ADVICE: dict[UsagePurpose, str] = {
    UsagePurpose.GAMING_GPU_INTENSIVE: "Bu profilde performansı GPU belirliyor — 4K/ray tracing gibi görsel yükte CPU farkı neredeyse hissedilmez, bütçeni ekran kartına ayır.",
    UsagePurpose.GAMING_CPU_INTENSIVE: "Simülasyon, strateji ve rekabetçi oyunlarda darboğaz genelde CPU'dur — güçlü bir GPU tek başına FPS'i kurtarmaz.",
    UsagePurpose.GAMING_BALANCED: "Genel oyun kullanımında CPU ve GPU dengeli çalışır, ikisi arasında büyük bir uçurum olmamasına dikkat et.",
    UsagePurpose.VIDEO_EDITING: "Modern kurgu yazılımlarında (Premiere, DaVinci) GPU hızlandırma öne çıkıyor — güçlü bir GPU render sürelerini doğrudan kısaltır.",
    UsagePurpose.SOFTWARE_DEVELOPMENT: "Derleme ve local ortamlar CPU çekirdek sayısına ve RAM'e bağlıdır, GPU bu senaryoda neredeyse hiç fark yaratmaz.",
}

class OptimizerService:
    def __init__(self, repository: HardwareRepository) -> None:
        self.repository = repository

    def analyze(self, gear: GearInput) -> GearOutput:

        cpu = self.repository.get_cpu_by_id(gear.cpu_id)
        gpu = self.repository.get_gpu_by_id(gear.gpu_id)
        ram = self.repository.get_ram_by_id(gear.ram_id)
        resolution = self.repository.get_resolution_by_id(gear.resolution_id)

        self._validate_component(cpu, gpu, ram, resolution)

        gpu_score_adjusted = int(gpu.score / resolution.demand_multiplier)

        weights = WEIGHTS[gear.usage_purpose]
        total_score = int(
            cpu.score * weights["cpu"]
            + gpu_score_adjusted * weights["gpu"]
            + ram.score * weights["ram"]
        )
        level = self._calculate_level(total_score)
        advice = USAGE_ADVICE[gear.usage_purpose]
        bottleneck = self._detect_bottleneck(cpu.score, gpu_score_adjusted, weights)

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
                "cpu_weight": weights["cpu"],
                "gpu": f"{gpu.brand} {gpu.model}",
                "gpu_score_raw": gpu.score,
                "gpu_score_adjusted": gpu_score_adjusted,
                "gpu_weight": weights["gpu"],
                "ram": f"{ram.capacity_gb}GB {ram.speed_mhz}MHz",
                "ram_score": ram.score,
                "ram_weight": weights["ram"],
                "resolution": resolution.name,
                "demand_multiplier": resolution.demand_multiplier,
                "bottleneck": bottleneck,
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

    def _detect_bottleneck(self, cpu_score: int, gpu_score_adjusted: int, weights: dict) -> str:
        if weights["cpu"] < 0.15 or weights["gpu"] < 0.15:
            return "Bu profilde darboğaz analizi anlamlı değil (bileşenlerden biri zaten neredeyse etkisiz)."
        diff = cpu_score - gpu_score_adjusted
        if diff > 15:
            return f"GPU'n CPU'nun gerisinde kalıyor (CPU {cpu_score} / GPU {gpu_score_adjusted}) — darboğazın GPU."
        if diff < -15:
            return f"CPU'n GPU'nun gerisinde kalıyor (CPU {cpu_score} / GPU {gpu_score_adjusted}) — darboğazın CPU."
        return f"CPU ({cpu_score}) ve GPU ({gpu_score_adjusted}) skorların dengeli, belirgin bir darboğaz yok."





   
    

    
    
    
    

   