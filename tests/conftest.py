import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from app.database.database import Base, get_db
from app.database.models import CPU, GPU, RAM, Resolution
from app.main import app


def _load_fixtures(session: Session) -> None:
    session.add_all([
        CPU(id=1, brand="Intel", model="Core i9-13900K", cores=24, base_clock=3.0, score=86),
        CPU(id=2, brand="Intel", model="Core i3-12100", cores=4, base_clock=3.3, score=19),
        GPU(id=1, brand="NVIDIA", model="RTX 4090", vram_gb=24, score=98),
        GPU(id=2, brand="AMD", model="RX 6600", vram_gb=8, score=39),
        RAM(id=1, capacity_gb=32, speed_mhz=3200, score=70),
        Resolution(id=1, name="1080p", width=1920, height=1080, demand_multiplier=1.0),
        Resolution(id=2, name="2160p", width=3840, height=2160, demand_multiplier=1.8),
    ])
    session.commit()


@pytest.fixture
def db_session():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(bind=engine)
    TestingSession = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = TestingSession()
    _load_fixtures(session)
    try:
        yield session
    finally:
        session.close()
        engine.dispose()


@pytest.fixture
def client(db_session):
    app.dependency_overrides[get_db] = lambda: db_session
    yield TestClient(app)
    app.dependency_overrides.clear()
