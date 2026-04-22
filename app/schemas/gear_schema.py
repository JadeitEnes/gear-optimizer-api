from pydantic import BaseModel, Field
from typing import Optional

class GearInput(BaseModel):
    cpu_id: int = Field(..., title="CPU", description="CPU ID seçin")
    gpu_id: int = Field(..., title="GPU", description="GPU ID seçin")
    ram_id: int = Field(..., title="RAM", description="RAM ID seçin")
    resolution_id: int = Field(..., title="Çözünürlük", description="Çözünürlük ID")
    usage_purpose: str = Field(..., title="Kullanım Amacı", description="oyun, video düzenleme, yazılım geliştirme")

class GearOutput(BaseModel):
    score:int = Field(..., title="Performans Skoru")
    level:str = Field(..., title="Seviye")
    advice:str = Field(..., title="Tavsiye")
    detail:dict = Field(..., title="Detay")

class CPUResponse(BaseModel):
    id:int
    brand: str
    model: str
    cores: int
    base_clock: float
    score: int

    class Config:
        from_attributes = True

class GPUResponse(BaseModel):
    id: int
    brand: str
    model: str
    vram_gb: int
    score: int

    class Config:
        from_attributes = True

class RamResponse(BaseModel):
    id: int
    capacity_gb: int
    speed_mhz: int
    score: int

    class Config:
        from_attributes = True

class ResolutionResponse(BaseModel):
    id: int
    name: str
    width: int 
    height: int
    demand_multiplier: float

    class Config:
        from_attributes = True
        

    


