from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, UniqueConstraint
from app.database.database import Base

class CPU(Base):
    __tablename__ ="cpus"
    id = Column(Integer, primary_key=True, index=True)
    brand = Column(String, nullable=False)
    model = Column(String, nullable=False, unique=True)
    cores = Column(Integer, nullable=False)
    base_clock = Column(Float, nullable=False)
    score = Column(Integer, nullable=False)

class GPU(Base):
    __tablename__ = "gpus"

    id = Column(Integer, primary_key=True, index=True)
    brand = Column(String, nullable=False)
    model = Column(String, nullable=False, unique=True)
    vram_gb= Column(Integer, nullable=False)
    score = Column(Integer, nullable=False)

class RAM(Base):
    __tablename__ = "rams"
    __table_args__ = (UniqueConstraint("capacity_gb", "speed_mhz"),)

    id = Column(Integer, primary_key=True, index=True)
    capacity_gb= Column(Integer, nullable=False)
    speed_mhz = Column(Integer, nullable=False)
    score = Column(Integer, nullable=False)

class Resolution(Base):
    __tablename__ = "resolutions"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True)
    width = Column(Integer, nullable=False)
    height = Column(Integer, nullable=False)
    demand_multiplier = Column(Float, nullable=False)

class SharedBuild(Base):
    __tablename__ = "shared_builds"

    id = Column(Integer, primary_key=True, index=True)
    slug = Column(String, nullable=False, unique=True, index=True)
    cpu_id = Column(Integer, ForeignKey("cpus.id"), nullable=False)
    gpu_id = Column(Integer, ForeignKey("gpus.id"), nullable=False)
    ram_id = Column(Integer, ForeignKey("rams.id"), nullable=False)
    resolution_id = Column(Integer, ForeignKey("resolutions.id"), nullable=False)
    usage_purpose = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))
