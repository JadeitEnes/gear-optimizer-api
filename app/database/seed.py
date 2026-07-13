from app.database.database import SessionLocal, engine
from app.database.models import Base, CPU, GPU, RAM, Resolution

def seed_data():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    
    cpus = [
        CPU(brand="Intel", model="Core Ultra 9 285K", cores=24, base_clock=3.7, score=100),
        CPU(brand="AMD", model="Ryzen 9 9950X", cores=16, base_clock=4.3, score=98),
        CPU(brand="AMD", model="Ryzen 9 7950X", cores=16, base_clock=4.5, score=92),
        CPU(brand="Intel", model="Core Ultra 7 265K", cores=20, base_clock=3.9, score=87),
        CPU(brand="Intel", model="Core i9-13900K", cores=24, base_clock=3.0, score=86),
        CPU(brand="AMD", model="Ryzen 9 9900X", cores=12, base_clock=4.4, score=81),
        CPU(brand="Intel", model="Core i7-13700K", cores=16, base_clock=3.4, score=68),
        CPU(brand="Intel", model="Core Ultra 5 245K", cores=14, base_clock=4.2, score=64),
        CPU(brand="AMD", model="Ryzen 7 9800X3D", cores=8, base_clock=4.3, score=59),
        CPU(brand="AMD", model="Ryzen 9 5900X", cores=12, base_clock=3.7, score=58),
        CPU(brand="Intel", model="Core i5-13600K", cores=14, base_clock=3.5, score=56),
        CPU(brand="AMD", model="Ryzen 7 9700X", cores=8, base_clock=3.8, score=55),
        CPU(brand="AMD", model="Ryzen 7 7700X", cores=8, base_clock=4.5, score=53),
        CPU(brand="AMD", model="Ryzen 7 7800X3D", cores=8, base_clock=4.2, score=51),
        CPU(brand="AMD", model="Ryzen 5 9600X", cores=6, base_clock=3.9, score=45),
        CPU(brand="AMD", model="Ryzen 7 5800X3D", cores=8, base_clock=3.4, score=42),
        CPU(brand="AMD", model="Ryzen 5 7600X", cores=6, base_clock=4.7, score=42),
        CPU(brand="AMD", model="Ryzen 7 5800X", cores=8, base_clock=3.8, score=41),
        CPU(brand="AMD", model="Ryzen 5 5600X", cores=6, base_clock=3.7, score=32),
        CPU(brand="Intel", model="Core i5-12400", cores=6, base_clock=2.5, score=28),
        CPU(brand="Intel", model="Core i3-12100", cores=4, base_clock=3.3, score=19),
    ]

    gpus = [
        GPU(brand="NVIDIA", model="RTX 5090",         vram_gb=32, score=100),
        GPU(brand="NVIDIA", model="RTX 4090",         vram_gb=24, score=98),
        GPU(brand="NVIDIA", model="RTX 5080",         vram_gb=16, score=92),
        GPU(brand="NVIDIA", model="RTX 5070 Ti",      vram_gb=16, score=83),
        GPU(brand="NVIDIA", model="RTX 4070 Ti Super",vram_gb=16, score=82),
        GPU(brand="AMD",    model="RX 7900 XTX",      vram_gb=24, score=81),
        GPU(brand="NVIDIA", model="RTX 4070 Super",   vram_gb=12, score=77),
        GPU(brand="AMD",    model="RX 7900 XT",       vram_gb=20, score=75),
        GPU(brand="NVIDIA", model="RTX 5070",         vram_gb=12, score=74),
        GPU(brand="AMD",    model="RX 9070 XT",       vram_gb=16, score=69),
        GPU(brand="AMD",    model="RX 9070",          vram_gb=16, score=65),
        GPU(brand="AMD",    model="RX 6800 XT",       vram_gb=16, score=64),
        GPU(brand="AMD",    model="RX 7800 XT",       vram_gb=16, score=63),
        GPU(brand="NVIDIA", model="RTX 5060 Ti 16GB", vram_gb=16, score=58),
        GPU(brand="NVIDIA", model="RTX 4060 Ti 16GB", vram_gb=16, score=58),
        GPU(brand="NVIDIA", model="RTX 5060 Ti 8GB",  vram_gb=8,  score=57),
        GPU(brand="NVIDIA", model="RTX 3070",         vram_gb=8,  score=57),
        GPU(brand="NVIDIA", model="RTX 5060",         vram_gb=8,  score=53),
        GPU(brand="NVIDIA", model="RTX 3060 Ti",      vram_gb=8,  score=52),
        GPU(brand="AMD",    model="RX 9060 XT",       vram_gb=16, score=52),
        GPU(brand="AMD",    model="RX 6700 XT",       vram_gb=12, score=51),
        GPU(brand="NVIDIA", model="RTX 4060",         vram_gb=8,  score=50),
        GPU(brand="AMD",    model="RX 6650 XT",       vram_gb=8,  score=44),
        GPU(brand="NVIDIA", model="RTX 5050",         vram_gb=8,  score=44),
        GPU(brand="NVIDIA", model="RTX 3060",         vram_gb=12, score=43),
        GPU(brand="AMD",    model="RX 6600",          vram_gb=8,  score=39),
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

    try:
        for cpu in cpus:
            if not db.query(CPU).filter(CPU.model == cpu.model).first():
                db.add(cpu)
                print(f"[SEED] Yeni CPU eklendi: {cpu.model}")

        for gpu in gpus:
            if not db.query(GPU).filter(GPU.model == gpu.model).first():
                db.add(gpu)
                print(f"[SEED] Yeni GPU eklendi: {gpu.model}")

        for ram in rams:
            if not db.query(RAM).filter(RAM.capacity_gb == ram.capacity_gb, RAM.speed_mhz == ram.speed_mhz).first():
                db.add(ram)
                print(f"[SEED] Yeni RAM eklendi: {ram.capacity_gb}GB {ram.speed_mhz}MHz")

        for res in resolutions:
            if not db.query(Resolution).filter(Resolution.name == res.name).first():
                db.add(res)
                print(f"[SEED] Yeni Çözünürlük eklendi: {res.name}")

        db.commit()
        print("Seed data added successfully.")
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()
