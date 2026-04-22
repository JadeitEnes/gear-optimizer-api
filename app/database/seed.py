from app.database.database import SessionLocal, engine
from app.database.models import Base, CPU, GPU, RAM, Resolution

def seed_data():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    if db.query(CPU).first():
        print("Data already exists, skipping seed.")
        db.close()
        return
    

    cpus = [
        CPU(brand="Intel", model="Core i9-13900k", cores=24, base_clock=3.0, score=95),
        CPU(brand="Intel", model="Core i7-13700k", cores=16, base_clock=3.4, score=85),
        CPU(brand="Intel", model="Core i5-13600k", cores=14, base_clock=3.5, score=75),
        CPU(brand="Intel", model="Core i5-12400", cores=6, base_clock=2.5, score=60),
        CPU(brand="Intel", model="Core i3-12100", cores=4, base_clock=3.3, score=45),
        CPU(brand="AMD", model="Ryzen 9 7950x", cores=16, base_clock=4.5, score=98),
        CPU(brand="AMD", model="Ryzen 9 5900X", cores=12, base_clock=3.7, score=88),
        CPU(brand="AMD", model="Ryzen 7 7700X", cores=8,  base_clock=4.5, score=80),
        CPU(brand="AMD", model="Ryzen 5 7600X", cores=6,  base_clock=4.7, score=70),
        CPU(brand="AMD", model="Ryzen 5 5600X", cores=6,  base_clock=3.7, score=62)

    ]

    gpus = [
        GPU(brand="NVIDIA", model="RTX 4090",    vram_gb=24, score=100),
        GPU(brand="NVIDIA", model="RTX 4080",    vram_gb=16, score=90),
        GPU(brand="NVIDIA", model="RTX 4070 Ti", vram_gb=12, score=82),
        GPU(brand="NVIDIA", model="RTX 4070",    vram_gb=12, score=75),
        GPU(brand="NVIDIA", model="RTX 3080",    vram_gb=10, score=70),
        GPU(brand="AMD", model="RX 7900 XTX",    vram_gb=24, score=88),
        GPU(brand="AMD", model="RX 7900 XT",     vram_gb=20, score=80),
        GPU(brand="AMD", model="RX 7800 XT",     vram_gb=16, score=68),
        GPU(brand="AMD", model="RX 6800 XT",     vram_gb=16, score=65),
        GPU(brand="AMD", model="RX 6700 XT",     vram_gb=12, score=55),
    ]

    rams = [
        RAM(capacity_gb=8, speed_mhz=3200, score=30),
        RAM(capacity_gb=16, speed_mhz=3200, score=50),
        RAM(capacity_gb=16, speed_mhz=4800, score=55),
        RAM(capacity_gb=32, speed_mhz=3200, score=70),
        RAM(capacity_gb=64, speed_mhz=4800, score=90),
    ]

    resolutions = [
        Resolution(name="1080p", width=1920, height=1080, demand_multiplier=1.0),
        Resolution(name="1440p", width=2560, height=1440, demand_multiplier=1.3),
        Resolution(name="2160p", width=3840, height=2160, demand_multiplier=1.8),
    ]

    db.add_all(cpus)
    db.add_all(gpus)
    db.add_all(rams)
    db.add_all(resolutions)
    db.commit()
    print("Seed data added successfully.")
    
    