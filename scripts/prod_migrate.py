import sys
import os
from sqlalchemy import create_engine, text

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

DATABASE_URL = os.environ.get("DATABASE_URL")
if not DATABASE_URL:
    print("HATA: DATABASE_URL env degiskeni bos. Render'daki EXTERNAL Database URL'i verin.")
    print('Ornek: $env:DATABASE_URL = "postgresql+psycopg2://...@dpg-xxxx.oregon-postgres.render.com/gear_db_vqpz"')
    sys.exit(1)
if "sqlite" in DATABASE_URL:
    print("HATA: sqlite'a bagli, production degil. Durduruluyor.")
    sys.exit(1)

engine = create_engine(DATABASE_URL)

with engine.connect() as conn:
    print("=== ONCESI: satir sayilari ===")
    for table in ["cpus", "gpus", "rams", "resolutions"]:
        count = conn.execute(text(f"SELECT COUNT(*) FROM {table}")).scalar()
        print(f"{table}: {count}")

    print("\n=== ONCESI: duplicate modeller ===")
    for table in ["gpus", "cpus"]:
        rows = conn.execute(text(
            f"SELECT model, COUNT(*) c FROM {table} GROUP BY model HAVING COUNT(*) > 1 ORDER BY c DESC"
        )).fetchall()
        for row in rows:
            print(f"{table} DUP -> {row[0]}: {row[1]} adet")
        if not rows:
            print(f"{table}: duplicate yok")

    print("\n=== Migration: TRUNCATE + UNIQUE constraint ===")
    conn.execute(text("TRUNCATE TABLE cpus, gpus, rams, resolutions RESTART IDENTITY"))
    conn.execute(text("ALTER TABLE cpus ADD CONSTRAINT uq_cpus_model UNIQUE (model)"))
    conn.execute(text("ALTER TABLE gpus ADD CONSTRAINT uq_gpus_model UNIQUE (model)"))
    conn.execute(text("ALTER TABLE rams ADD CONSTRAINT uq_rams_capacity_speed UNIQUE (capacity_gb, speed_mhz)"))
    conn.execute(text("ALTER TABLE resolutions ADD CONSTRAINT uq_resolutions_name UNIQUE (name)"))
    conn.commit()
    print("Migration tamamlandi.")

print("\n=== Yeni veri ekleniyor (seed_data) ===")
os.environ["DATABASE_URL"] = DATABASE_URL
from app.database.seed import seed_data
seed_data()

with engine.connect() as conn:
    print("\n=== SONRASI: satir sayilari ===")
    for table in ["cpus", "gpus", "rams", "resolutions"]:
        count = conn.execute(text(f"SELECT COUNT(*) FROM {table}")).scalar()
        print(f"{table}: {count}")

    print("\n=== SONRASI: duplicate kontrolu ===")
    for table in ["gpus", "cpus"]:
        rows = conn.execute(text(
            f"SELECT model, COUNT(*) c FROM {table} GROUP BY model HAVING COUNT(*) > 1"
        )).fetchall()
        print(f"{table}: {'duplicate yok' if not rows else rows}")
