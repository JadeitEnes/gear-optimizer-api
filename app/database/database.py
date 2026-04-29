import logging
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from typing import Generator
from app.config import get_settings

logger = logging.getLogger(__name__)

settings = get_settings()

def _build_engine():

 if "sqlite" in settings.database_url:
    logger.info("Using SQLite database")
    return create_engine(
        settings.database_url,
        connect_args={"check_same_thread": False}
    )
 logger.info("Using PostgreSQL database")
 return create_engine(settings.database_url)

engine = _build_engine()

SessionLocal = sessionmaker(
   autocommit = False,
   autoflush=False,
   bind=engine
)
  

Base = declarative_base()
def get_db() -> Generator[Session, None, None]:

 
    db = SessionLocal()
    try:
        yield db
    except Exception as e:
       logger.error(f"Database session error: {e}")
       db.rollback()
       raise    
    finally:
        db.close()    