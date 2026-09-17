from app.schemas.gear_schema import BuildComparison, BuildComparisonSide, GearInput, GearOutput
from app.services.optimizer_service import OptimizerService

DRIVER_FIELDS = {
    "CPU": ("cpu_score", "cpu_weight"),
    "GPU": ("gpu_score_adjusted", "gpu_weight"),
    "RAM": ("ram_score", "ram_weight"),
}


class ComparisonService:
    def __init__(self, optimizer: OptimizerService) -> None:
        self.optimizer = optimizer

    def compare(self, build_a: GearInput, build_b: GearInput) -> BuildComparison:
        result_a = self.optimizer.analyze(build_a)
        result_b = self.optimizer.analyze(build_b)

        winner = self._winner(result_a.score, result_b.score)
        score_diff = abs(result_a.score - result_b.score)

        return BuildComparison(
            build_a=BuildComparisonSide(result=result_a),
            build_b=BuildComparisonSide(result=result_b),
            winner=winner,
            score_diff=score_diff,
            explanation=self._explain(result_a, result_b, winner, score_diff),
            cpu_winner=self._winner(result_a.detail["cpu_score"], result_b.detail["cpu_score"]),
            gpu_winner=self._winner(result_a.detail["gpu_score_adjusted"], result_b.detail["gpu_score_adjusted"]),
            ram_winner=self._winner(result_a.detail["ram_score"], result_b.detail["ram_score"]),
        )

    def _winner(self, value_a: float, value_b: float) -> str:
        if value_a > value_b:
            return "a"
        if value_b > value_a:
            return "b"
        return "tie"

    def _explain(self, result_a: GearOutput, result_b: GearOutput, winner: str, score_diff: int) -> str:
        if winner == "tie":
            return "İki sistem de aynı puanı alıyor, performans açısından fark yok."

        winner_label = "Sistem A" if winner == "a" else "Sistem B"
        winner_detail = result_a.detail if winner == "a" else result_b.detail
        loser_detail = result_b.detail if winner == "a" else result_a.detail

        contributions = {
            name: winner_detail[score_key] * winner_detail[weight_key] - loser_detail[score_key] * loser_detail[weight_key]
            for name, (score_key, weight_key) in DRIVER_FIELDS.items()
        }
        driver = max(contributions, key=contributions.get)
        driver_diff = round(contributions[driver])
        driver_weight_pct = round(winner_detail[DRIVER_FIELDS[driver][1]] * 100)

        return (
            f"{winner_label} kazanıyor (+{score_diff} puan) — farkın +{driver_diff} puanı {driver}'dan geliyor, "
            f"bu profilde {driver}'nun ağırlığı %{driver_weight_pct} olduğu için en belirleyici bileşen o."
        )
