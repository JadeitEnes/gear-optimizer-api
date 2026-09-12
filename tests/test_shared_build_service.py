import pytest
from sqlalchemy.exc import IntegrityError

from app.database.models import SharedBuild
from app.enums import UsagePurpose
from app.exceptions import ComponentNotFoundError
from app.repositories.hardware_repository import HardwareRepository
from app.repositories.shared_build_repository import SharedBuildRepository
from app.schemas.gear_schema import GearInput
from app.services.optimizer_service import OptimizerService
from app.services.shared_build_service import SharedBuildService


def _service(db_session) -> SharedBuildService:
    hardware = HardwareRepository(db_session)
    return SharedBuildService(SharedBuildRepository(db_session), OptimizerService(hardware))


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


def test_create_share_persists_and_returns_a_slug(db_session):
    build = _service(db_session).create_share(_gear())

    assert build.slug
    assert build.cpu_id == 1
    assert build.gpu_id == 1
    assert build.ram_id == 1
    assert build.resolution_id == 1
    assert build.usage_purpose == "gaming_balanced"


def test_create_share_rejects_unknown_component(db_session):
    with pytest.raises(ComponentNotFoundError):
        _service(db_session).create_share(_gear(cpu_id=999))


def test_get_by_slug_returns_the_matching_build(db_session):
    created = _service(db_session).create_share(_gear(gpu_id=2))

    found = SharedBuildRepository(db_session).get_by_slug(created.slug)

    assert found is not None
    assert found.id == created.id
    assert found.gpu_id == 2


def test_get_by_slug_returns_none_for_unknown_slug(db_session):
    assert SharedBuildRepository(db_session).get_by_slug("does-not-exist") is None


def test_repository_retries_on_slug_collision(db_session, monkeypatch):
    repository = SharedBuildRepository(db_session)
    tokens = iter(["dup", "dup", "unique"])
    monkeypatch.setattr(
        "app.repositories.shared_build_repository.secrets.token_urlsafe",
        lambda n: next(tokens),
    )

    first = repository.create(cpu_id=1, gpu_id=1, ram_id=1, resolution_id=1, usage_purpose="gaming_balanced")
    assert first.slug == "dup"

    second = repository.create(cpu_id=1, gpu_id=1, ram_id=1, resolution_id=1, usage_purpose="gaming_balanced")
    assert second.slug == "unique"


def test_foreign_key_constraint_rejects_unknown_cpu_id(db_session):
    db_session.add(SharedBuild(
        slug="raw-insert", cpu_id=999, gpu_id=1, ram_id=1, resolution_id=1, usage_purpose="gaming_balanced",
    ))
    with pytest.raises(IntegrityError):
        db_session.commit()
