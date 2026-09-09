import pytest

from app.enums import UsagePurpose
from app.exceptions import ComponentNotFoundError
from app.repositories.hardware_repository import HardwareRepository
from app.schemas.gear_schema import GearInput
from app.services.optimizer_service import OptimizerService


def _analyze(db_session, **overrides):
    payload = {
        "cpu_id": 1,
        "gpu_id": 1,
        "ram_id": 1,
        "resolution_id": 1,
        "usage_purpose": UsagePurpose.GAMING_BALANCED,
    }
    payload.update(overrides)
    service = OptimizerService(HardwareRepository(db_session))
    return service.analyze(GearInput(**payload))


def test_score_uses_profile_weights(db_session):
    result = _analyze(db_session)

    assert result.score == 88
    assert result.level == "Profesyonel"
    assert result.detail["cpu_weight"] == 0.35
    assert result.detail["gpu_weight"] == 0.45


def test_same_build_scores_lower_at_higher_resolution(db_session):
    at_1080p = _analyze(db_session, resolution_id=1)
    at_2160p = _analyze(db_session, resolution_id=2)

    assert at_2160p.score < at_1080p.score
    assert at_2160p.detail["gpu_score_raw"] == 98
    assert at_2160p.detail["gpu_score_adjusted"] == 54


def test_profile_change_reweights_same_hardware(db_session):
    gpu_heavy = _analyze(db_session, usage_purpose=UsagePurpose.GAMING_GPU_INTENSIVE)
    cpu_heavy = _analyze(db_session, usage_purpose=UsagePurpose.GAMING_CPU_INTENSIVE)

    assert gpu_heavy.score > cpu_heavy.score
    assert gpu_heavy.advice != cpu_heavy.advice


def test_weak_cpu_is_reported_as_bottleneck(db_session):
    result = _analyze(db_session, cpu_id=2, gpu_id=1)

    assert "darboğazın CPU" in result.detail["bottleneck"]


def test_weak_gpu_is_reported_as_bottleneck(db_session):
    result = _analyze(db_session, cpu_id=1, gpu_id=2)

    assert "darboğazın GPU" in result.detail["bottleneck"]


def test_balanced_build_reports_no_bottleneck(db_session):
    result = _analyze(db_session, cpu_id=1, gpu_id=1, resolution_id=1)

    assert "belirgin bir darboğaz yok" in result.detail["bottleneck"]


def test_bottleneck_skipped_when_component_barely_weighted(db_session):
    result = _analyze(db_session, usage_purpose=UsagePurpose.SOFTWARE_DEVELOPMENT)

    assert "anlamlı değil" in result.detail["bottleneck"]


@pytest.mark.parametrize(
    "overrides, missing",
    [
        ({"cpu_id": 999}, "CPU"),
        ({"gpu_id": 999}, "GPU"),
        ({"ram_id": 999}, "RAM"),
        ({"resolution_id": 999}, "Resolution"),
    ],
)
def test_unknown_component_raises(db_session, overrides, missing):
    with pytest.raises(ComponentNotFoundError) as exc_info:
        _analyze(db_session, **overrides)

    assert exc_info.value.missing == [missing]
