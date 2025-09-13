from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from typing import Generator

from app.models import Base

# TODO: use Pydantic's PostgresDsn
# TODO: remove hardcoded strings (use config.py and .env file) - https://github.com/fastapi/full-stack-fastapi-template/blob/master/backend/app/core/db.py

DATABASE_URL = "postgresql+psycopg2://test:1234@localhost:5432/mydb"

engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db() -> None:
    Base.metadata.create_all(engine)
    
def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()