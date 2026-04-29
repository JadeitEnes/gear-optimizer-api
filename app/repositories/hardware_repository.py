import logging 
from sqlalchemy.orm import Session
from typing import Optional
from app.database.models import CPU, GPU, RAM, Resolution

logger = logging.getLogger(__name__)

class HardwareRepository:

    def __init__(self, db: Session) -> None:
        self.db = db

    def get_all_cpus(self) -> list[CPU]:
        logger.debug("Fetching all CPUs")
        return self.db.query(CPU).all()

    def get_all_gpus(self) -> list [GPU]:
        logger.debug("Fetching all GPUs")
        return self.db.query(GPU).all() 
       
    def get_all_rams(self) -> list [RAM]:
        logger.debug("Fetching all RAMs")
        return self.db.query(RAM).all()
    
    def get_all_resolutions(self) -> list [Resolution]:
        logger.debug("Fetching all Resolutions")
        return self.db.query(Resolution).all()
    
    def get_cpu_by_id(self, cpu_id: int) -> Optional[CPU]:
        logger.debug(f"Fetching CPU with id={cpu_id}")
        return self.db.query(CPU).filter(CPU.id == cpu_id).first()
    
    def get_gpu_by_id(self, gpu_id: int) -> Optional[GPU]:
        logger.debug(f"Fetching GPU with id={gpu_id}")
        return self.db.query(GPU).filter(GPU.id == gpu_id).first()

    def get_ram_by_id(self, ram_id: int) -> Optional[RAM]:
        logger.debug(f"Fetching RAM with id={ram_id}")
        return self.db.query(RAM).filter(RAM.id == ram_id).first()    
    
    def get_resolution_by_id(self, resolution_id: int) -> Optional[Resolution]:
        logger.debug(f"Fetching Resolution with id={resolution_id}")
        return self.db.query(Resolution).filter(Resolution.id == resolution_id).first()
        
