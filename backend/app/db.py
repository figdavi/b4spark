from sqlalchemy import create_engine
from app.models import Base

# TODO: use Pydantic's PostgresDsn
# TODO: remove hardcoded strings (use config.py and .env file) - https://github.com/fastapi/full-stack-fastapi-template/blob/master/backend/app/core/db.py

DATABASE_URL = "postgresql+psycopg2://test:1234@localhost:5432/mydb"

engine = create_engine(DATABASE_URL, echo=True)

def init_db() -> None:
    Base.metadata.create_all(engine)