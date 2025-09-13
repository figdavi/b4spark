from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.models import Sensor, SensorCreate, SensorOut
from app.db import get_db

router = APIRouter(
    prefix="/sensors",
    tags=["sensors"],
    dependencies=[],
    responses={404: {"description": "Not found"}},
)


@router.get("/", status_code=200, response_model=list[SensorOut])
async def read_sensors(session: Session = Depends(get_db)) -> list[SensorOut]:
    """Retrieve sensors.

    Returns:
        list[Sensor]: a list containing the sensors.
    """
    sensors = session.scalars(select(Sensor).order_by(Sensor.id)).all()
    
    return [SensorOut.model_validate(sensor) for sensor in sensors]


@router.post("/", status_code=201, response_model=SensorOut)
async def create_sensor(
    data: SensorCreate,
    session: Session = Depends(get_db),
) -> SensorOut:
    new_sensor = Sensor(**data.model_dump())

    session.add(new_sensor)
    session.commit()

    return SensorOut.model_validate(new_sensor)
