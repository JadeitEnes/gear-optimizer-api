from pydantic import BaseModel, Field
from typing import Optional

class GearInput(BaseModel):
    cpu_brand: str = Field(..., title="CPU Markası", description="İşlemci markası (örn: Intel, AMD)")
    cpu_cores: int = Field(..., title="CPU Çekirdek Sayısı", description="İşlemci çekirdek sayısı")
    ram_gb: int = Field(..., title="RAM (GB)", description="Bellek miktarı gigabayt cinsinden")
    gpu_brand: Optional[str] = Field(None, title="GPU Markası", description="Ekran kartı markası (örn: NVIDIA, AMD, Intel)")
    usage_purpose: str = Field(..., title="Kullanım Amacı", description="Örn: oyun, video düzenleme, yazılım geliştirme")

class GearOutput(BaseModel):
    score:int = Field(..., title="Performans Skoru", description="100 üzerinden hesaplanan skor")
    level:str = Field(..., title="Seviye",description="Giriş,Orta,Üst veya Profesyonel")
    advice:str = Field(..., title="Tavsiye",description="Donanım hakkında öneri")
    detail:dict = Field(..., title="Detay",description="Bileşen analizi")
    


