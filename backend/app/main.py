from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.db import init_db
from app.api.main import api_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(api_router)


@app.get("/")
def root():
    return {"message": "test"}
