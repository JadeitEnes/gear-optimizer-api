from app.database.models import CPU, GPU, RAM
from app.enums import UsagePurpose
from app.repositories.hardware_repository import HardwareRepository
from app.schemas.gear_schema import GearInput
from app.services.optimizer_service import OptimizerService
from app.services.upgrade_advisor_service import UpgradeAdvisorService


def _advisor(db_session) -> UpgradeAdvisorService:
    repository = HardwareRepository(db_session)
    return UpgradeAdvisorService(repository, OptimizerService(repository))


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


def test_suggests_the_nearest_better_cpu(db_session):
    advice = _advisor(db_session).advise(_gear(cpu_id=1))

    cpu_option = next(o for o in advice.options if o.component == "cpu")
    assert cpu_option.suggested == "Intel Core Ultra 9 285K"
    assert cpu_option.score_gain > 0
    assert cpu_option.cost_index == 1.0


def test_component_at_top_tier_has_no_suggestion(db_session):
    advice = _advisor(db_session).advise(_gear(cpu_id=3))

    cpu_option = next(o for o in advice.options if o.component == "cpu")
    assert cpu_option.suggested is None
    assert cpu_option.score_gain == 0
    assert cpu_option.efficiency == 0.0
    assert "en üst modeldesin" in cpu_option.note


def test_best_pick_is_none_when_every_component_is_maxed(db_session):
    advice = _advisor(db_session).advise(_gear(cpu_id=3, gpu_id=3, ram_id=2))

    assert advice.best_pick is None
    assert all(option.score_gain == 0 for option in advice.options)


def test_options_are_sorted_by_efficiency_descending(db_session):
    advice = _advisor(db_session).advise(_gear(cpu_id=1, gpu_id=2, ram_id=1))

    efficiencies = [option.efficiency for option in advice.options]
    assert efficiencies == sorted(efficiencies, reverse=True)
    assert advice.best_pick == advice.options[0]


def test_ram_cost_index_can_outrank_a_larger_raw_gain(db_session):
    db_session.add_all([
        CPU(brand="Bench", model="CPU-Base", cores=1, base_clock=1.0, score=200),
        CPU(brand="Bench", model="CPU-Next", cores=1, base_clock=1.0, score=220),
        GPU(brand="Bench", model="GPU-Base", vram_gb=1, score=200),
        GPU(brand="Bench", model="GPU-Next", vram_gb=1, score=220),
        RAM(capacity_gb=1, speed_mhz=1, score=200),
        RAM(capacity_gb=2, speed_mhz=2, score=250),
    ])
    db_session.commit()

    cpu_base = db_session.query(CPU).filter_by(model="CPU-Base").one()
    gpu_base = db_session.query(GPU).filter_by(model="GPU-Base").one()
    ram_base = db_session.query(RAM).filter_by(score=200).one()

    gear = _gear(cpu_id=cpu_base.id, gpu_id=gpu_base.id, ram_id=ram_base.id)
    advice = _advisor(db_session).advise(gear)
    by_component = {option.component: option for option in advice.options}

    assert by_component["ram"].score_gain == 10
    assert by_component["gpu"].score_gain == 9
    assert by_component["gpu"].efficiency > by_component["ram"].efficiency
    assert advice.best_pick.component == "gpu"


def test_gpu_upgrade_uses_raw_score_not_resolution_adjusted_score(db_session):
    advice = _advisor(db_session).advise(_gear(gpu_id=1, resolution_id=2))

    gpu_option = next(o for o in advice.options if o.component == "gpu")
    assert gpu_option.suggested == "NVIDIA RTX 5090"
