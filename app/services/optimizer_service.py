from app.schemas.gear_schema import GearInput, GearOutput

CPU_SCORES = {
    "intel":40,
    "amd":38,

}


GPU_SCORES = {
    "nvidia":30,
    "amd":25,
    "intel":15,
}

USAGE_ADVICE = {
    "gaming": "Yüksek frekanslı RAM ve güçlü GPU önceliğiniz olmalı.",
    "video_editing": "Çok çekirdekli CPU ve 32GB+ RAM kritik önem taşıyor.",
    "software_development": "Hızlı SSD ve 16GB+ RAM geliştirme deneyimini doğrudan etkiler.",
}

def calculate_gear_score(gear:GearInput) -> GearOutput:
    cpu_score = CPU_SCORES.get(gear.cpu_brand.lower(),30)
    ram_score = min(gear.ram_gb,64)// 4
    gpu_score = 0
    if gear.gpu_brand:
        gpu_score=GPU_SCORES.get(gear.gpu_brand.lower(),10)
    core_score = min(gear.cpu_cores * 2, 20)    # Scoring Logic: 2 points per core, max 20 points.
    total_score = cpu_score + ram_score + gpu_score + core_score

    if total_score >= 80:
        level = "Profesyonel"
    elif total_score >= 60:
        level = "Üst Seviye"
    elif total_score >= 40:
        level = "Orta Seviye"
    else:
        level = "Giriş Seviye"    
    advice = USAGE_ADVICE.get(
        gear.usage_purpose.lower(),
        "Kullanım amacınıza özel tavsiye için geçerli bir amaç yazınız."
    )
    detail = {
        "cpu_score": cpu_score,
        "ram_score": ram_score,
        "gpu_score": gpu_score,
        "core_score": core_score,
    }

    return GearOutput(
        score = total_score,
        level = level,
        advice = advice,
        detail = detail,
    )