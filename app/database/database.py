import logging
from sqlalchemy import create_engine, event
from sqlalchemy.orm import declarative_base, sessionmaker, Session
from typing import Generator
from app.config import get_settings

logger = logging.getLogger(__name__)

settings = get_settings()

def _build_engine():

 if "sqlite" in settings.database_url:
    logger.info("Using SQLite database")
    sqlite_engine = create_engine(
        settings.database_url,
        connect_args={"check_same_thread": False}
    )
    event.listens_for(sqlite_engine, "connect")(enable_sqlite_foreign_keys)
    return sqlite_engine
 logger.info("Using PostgreSQL database")
 return create_engine(settings.database_url)


def enable_sqlite_foreign_keys(dbapi_connection, connection_record) -> None:
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()

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