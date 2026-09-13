import logging
from app.database.models import CPU, GPU, RAM
from app.repositories.hardware_repository import HardwareRepository
from app.schemas.gear_schema import GearInput, UpgradeAdvice, UpgradeOption
from app.services.optimizer_service import OptimizerService

logger = logging.getLogger(__name__)

MARKET_COST_INDEX: dict[str, float] = {
    "cpu": 1.0,
    "gpu": 1.0,
    "ram": 1.5,
}


class UpgradeAdvisorService:
    def __init__(self, repository: HardwareRepository, optimizer: OptimizerService) -> None:
        self.repository = repository
        self.optimizer = optimizer

    def advise(self, gear: GearInput) -> UpgradeAdvice:
        baseline_score = self.optimizer.analyze(gear).score

        options = [
            self._evaluate_cpu(gear, baseline_score),
            self._evaluate_gpu(gear, baseline_score),
            self._evaluate_ram(gear, baseline_score),
        ]
        options.sort(key=lambda option: option.efficiency, reverse=True)

        best_pick = options[0] if options[0].score_gain > 0 else None

        return UpgradeAdvice(baseline_score=baseline_score, options=options, best_pick=best_pick)

    def _evaluate_cpu(self, gear: GearInput, baseline_score: int) -> UpgradeOption:
        current = self.repository.get_cpu_by_id(gear.cpu_id)
        candidate = self.repository.get_next_better_cpu(current.score)
        return self._build_option(
            component="cpu",
            gear=gear,
            id_field="cpu_id",
            baseline_score=baseline_score,
            current_label=f"{current.brand} {current.model}",
            candidate=candidate,
            candidate_label=f"{candidate.brand} {candidate.model}" if candidate else None,
        )

    def _evaluate_gpu(self, gear: GearInput, baseline_score: int) -> UpgradeOption:
        current = self.repository.get_gpu_by_id(gear.gpu_id)
        candidate = self.repository.get_next_better_gpu(current.score)
        return self._build_option(
            component="gpu",
            gear=gear,
            id_field="gpu_id",
            baseline_score=baseline_score,
            current_label=f"{current.brand} {current.model}",
            candidate=candidate,
            candidate_label=f"{candidate.brand} {candidate.model}" if candidate else None,
        )

    def _evaluate_ram(self, gear: GearInput, baseline_score: int) -> UpgradeOption:
        current = self.repository.get_ram_by_id(gear.ram_id)
        candidate = self.repository.get_next_better_ram(current.score)
        return self._build_option(
            component="ram",
            gear=gear,
            id_field="ram_id",
            baseline_score=baseline_score,
            current_label=f"{current.capacity_gb}GB {current.speed_mhz}MHz",
            candidate=candidate,
            candidate_label=f"{candidate.capacity_gb}GB {candidate.speed_mhz}MHz" if candidate else None,
        )

    def _build_option(
        self,
        component: str,
        gear: GearInput,
        id_field: str,
        baseline_score: int,
        current_label: str,
        candidate: CPU | GPU | RAM | None,
        candidate_label: str | None,
    ) -> UpgradeOption:
        cost_index = MARKET_COST_INDEX[component]

        if candidate is None:
            return UpgradeOption(
                component=component,
                current=current_label,
                suggested=None,
                score_gain=0,
                cost_index=cost_index,
                efficiency=0.0,
                note="Zaten bu kategoride en üst modeldesin.",
            )

        hypothetical = gear.model_copy(update={id_field: candidate.id})
        new_score = self.optimizer.analyze(hypothetical).score
        gain = new_score - baseline_score
        efficiency = round(gain / cost_index, 1)

        logger.debug(f"{component} upgrade candidate: gain={gain}, cost_index={cost_index}, efficiency={efficiency}")

        return UpgradeOption(
            component=component,
            current=current_label,
            suggested=candidate_label,
            score_gain=gain,
            cost_index=cost_index,
            efficiency=efficiency,
            note=self._note_for(gain, candidate_label),
        )

    def _note_for(self, gain: int, candidate_label: str) -> str:
        if gain <= 0:
            return "Bu profilde bileşenin skora etkisi neredeyse yok, öncelik verme."
        return f"{candidate_label}'e geçersen skorun {gain} puan artar."
