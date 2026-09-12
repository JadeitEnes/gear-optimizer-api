from app.database.models import SharedBuild
from app.repositories.shared_build_repository import SharedBuildRepository
from app.schemas.gear_schema import GearInput
from app.services.optimizer_service import OptimizerService


class SharedBuildService:
    def __init__(self, repository: SharedBuildRepository, optimizer: OptimizerService) -> None:
        self.repository = repository
        self.optimizer = optimizer

    def create_share(self, gear: GearInput) -> SharedBuild:
        self.optimizer.analyze(gear)

        return self.repository.create(
            cpu_id=gear.cpu_id,
            gpu_id=gear.gpu_id,
            ram_id=gear.ram_id,
            resolution_id=gear.resolution_id,
            usage_purpose=gear.usage_purpose.value,
        )
