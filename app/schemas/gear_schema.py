from typing import Literal
from pydantic import BaseModel, ConfigDict, Field
from app.enums import UsagePurpose


class GearInput(BaseModel):
    cpu_id: int = Field(..., title="CPU", description="CPU ID seçin")
    gpu_id: int = Field(..., title="GPU", description="GPU ID seçin")
    ram_id: int = Field(..., title="RAM", description="RAM ID seçin")
    resolution_id: int = Field(..., title="Resolution", description="Çözünürlük ID")
    usage_purpose: UsagePurpose = Field(..., title="Kullanım Amacı")


class GearOutput(BaseModel):
    score: int = Field(..., title="Performans Skoru")
    level: str = Field(..., title="Seviye")
    advice: str = Field(..., title="Tavsiye")
    detail: dict = Field(..., title="Detay")


class CPUResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    brand: str
    model: str
    cores: int
    base_clock: float
    score: int


class GPUResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    brand: str
    model: str
    vram_gb: int
    score: int


class RamResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    capacity_gb: int
    speed_mhz: int
    score: int


class ResolutionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    width: int
    height: int
    demand_multiplier: float


class UpgradeOption(BaseModel):
    component: Literal["cpu", "gpu", "ram"] = Field(..., title="Bileşen")
    current: str = Field(..., title="Mevcut Model")
    suggested: str | None = Field(None, title="Önerilen Model", description="Zaten en üst modeldeyse null")
    score_gain: int = Field(..., title="Skor Kazancı", description="Bu yükseltmenin toplam skora katkısı")
    cost_index: float = Field(..., title="Maliyet Endeksi", description="Piyasa koşullarına göre elle ayarlanan göreli maliyet çarpanı")
    efficiency: float = Field(..., title="Verimlilik", description="score_gain / cost_index — sıralama bu değere göre yapılır")
    note: str = Field(..., title="Açıklama")


class UpgradeAdvice(BaseModel):
    baseline_score: int = Field(..., title="Mevcut Skor")
    options: list[UpgradeOption] = Field(..., title="Seçenekler")
    best_pick: UpgradeOption | None = Field(None, title="En Verimli Seçim", description="Hiçbir yükseltme skoru artırmıyorsa null")
