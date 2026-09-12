import logging
import secrets
from typing import Optional
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from app.database.models import SharedBuild

logger = logging.getLogger(__name__)

MAX_SLUG_ATTEMPTS = 5


class SharedBuildRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def create(self, cpu_id: int, gpu_id: int, ram_id: int, resolution_id: int, usage_purpose: str) -> SharedBuild:
        for attempt in range(1, MAX_SLUG_ATTEMPTS + 1):
            slug = secrets.token_urlsafe(6)
            build = SharedBuild(
                slug=slug,
                cpu_id=cpu_id,
                gpu_id=gpu_id,
                ram_id=ram_id,
                resolution_id=resolution_id,
                usage_purpose=usage_purpose,
            )
            self.db.add(build)
            try:
                self.db.commit()
            except IntegrityError:
                logger.warning(f"Slug collision on attempt {attempt}/{MAX_SLUG_ATTEMPTS}: {slug}")
                self.db.rollback()
                continue
            self.db.refresh(build)
            return build

        raise RuntimeError(f"Could not generate a unique share slug after {MAX_SLUG_ATTEMPTS} attempts")

    def get_by_slug(self, slug: str) -> Optional[SharedBuild]:
        logger.debug(f"Fetching shared build with slug={slug}")
        return self.db.query(SharedBuild).filter(SharedBuild.slug == slug).first()
