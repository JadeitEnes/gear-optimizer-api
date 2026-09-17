from app.enums import UsagePurpose
from app.repositories.hardware_repository import HardwareRepository
from app.schemas.gear_schema import GearInput
from app.services.comparison_service import ComparisonService
from app.services.optimizer_service import OptimizerService


def _service(db_session) -> ComparisonService:
    optimizer = OptimizerService(HardwareRepository(db_session))
    return ComparisonService(optimizer)


def _gear(**overrides) -> GearInput:
    payload = {
        "cpu_id": 1,
        "gpu_id": 1,
        "ram_id": 1,
        "resolution_id": 1,
        "usage_purpose": UsagePurpose.GAMING_BALANCED,
    }
    payload.update(overrides)
    return GearInput(**payload)


def test_stronger_build_wins_on_every_metric(db_session):
    build_a = _gear(cpu_id=3, gpu_id=3, ram_id=2)
    build_b = _gear(cpu_id=2, gpu_id=2, ram_id=1)

    result = _service(db_session).compare(build_a, build_b)

    assert result.build_a.result.score == 98
    assert result.build_b.result.score == 38
    assert result.winner == "a"
    assert result.score_diff == 60
    assert result.cpu_winner == "a"
    assert result.gpu_winner == "a"
    assert result.ram_winner == "a"
    assert "Sistem A" in result.explanation
    assert "CPU" in result.explanation
    assert "%" in result.explanation


def test_identical_builds_tie(db_session):
    build_a = _gear()
    build_b = _gear()

    result = _service(db_session).compare(build_a, build_b)

    assert result.winner == "tie"
    assert result.score_diff == 0
    assert result.cpu_winner == "tie"
    assert result.gpu_winner == "tie"
    assert result.ram_winner == "tie"
    assert "fark yok" in result.explanation


def test_per_metric_winner_is_independent_of_overall_winner(db_session):
    build_a = _gear(cpu_id=3, gpu_id=2, ram_id=1, usage_purpose=UsagePurpose.GAMING_GPU_INTENSIVE)
    build_b = _gear(cpu_id=2, gpu_id=3, ram_id=2, usage_purpose=UsagePurpose.GAMING_GPU_INTENSIVE)

    result = _service(db_session).compare(build_a, build_b)

    assert result.build_a.result.score == 57
    assert result.build_b.result.score == 81
    assert result.winner == "b"
    assert result.cpu_winner == "a"
    assert result.gpu_winner == "b"
    assert result.ram_winner == "b"


def test_gpu_comparison_uses_resolution_adjusted_score(db_session):
    build_a = _gear(gpu_id=1, resolution_id=1)
    build_b = _gear(gpu_id=1, resolution_id=2)

    result = _service(db_session).compare(build_a, build_b)

    assert result.build_a.result.detail["gpu"] == result.build_b.result.detail["gpu"]
    assert result.build_a.result.detail["gpu_score_adjusted"] == 98
    assert result.build_b.result.detail["gpu_score_adjusted"] == 54
    assert result.gpu_winner == "a"


def test_each_side_carries_its_own_bottleneck_and_breakdown(db_session):
    build_a = _gear(cpu_id=3, gpu_id=2)
    build_b = _gear(cpu_id=2, gpu_id=3)

    result = _service(db_session).compare(build_a, build_b)

    assert "bottleneck" in result.build_a.result.detail
    assert "bottleneck" in result.build_b.result.detail
    assert result.build_a.result.detail["bottleneck"] != result.build_b.result.detail["bottleneck"]
