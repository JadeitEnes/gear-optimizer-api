class GearOptimizerError(Exception):
    pass


class ComponentNotFoundError(GearOptimizerError):
    def __init__(self, missing: list[str]) -> None:
        self.missing = missing
        super().__init__(f"Geçersiz donanım ID'si: {', '.join(missing)}")


class SharedBuildNotFoundError(GearOptimizerError):
    def __init__(self, slug: str) -> None:
        self.slug = slug
        super().__init__(f"Paylaşım linki bulunamadı: {slug}")
