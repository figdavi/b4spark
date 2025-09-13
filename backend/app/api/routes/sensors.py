from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select
from random import randrange
from app.models import (
    Sensor,
    SensorCreate,
    SensorOut,
    SensorUpdate,
    Reading,
    ReadingOut,
)
from app.db import get_db

# ## Endpoints
# These are endpoints for the version without users, pdf and alerts.
# - GET /api/sensors
# - POST /api/sensors
# - GET /api/sensors/{sensor_id}
# - PATCH /api/sensors/{sensor_id}
# - GET /api/sensors/{sensor_id}/readings?start_period=DateTime&end_period=DateTime

router = APIRouter(
    prefix="/sensors",
    tags=["sensors"],
    dependencies=[],
    responses={404: {"description": "Not found"}},
)


@router.get("/", status_code=200, response_model=list[SensorOut])
async def read_sensors(session: Session = Depends(get_db)):
    """Retrieve sensors.

    Returns:
        list[Sensor]: a list containing the sensors.
    """
    sensors = session.scalars(select(Sensor).order_by(Sensor.id)).all()

    return sensors


@router.post("/", status_code=201, response_model=SensorOut)
async def create_sensor(
    data: SensorCreate,
    session: Session = Depends(get_db),
):
    new_sensor = Sensor(**data.model_dump())

    session.add(new_sensor)
    session.commit()

    return new_sensor


@router.patch("/{sensor_id}", response_model=SensorOut)
async def update_sensor(
    sensor_id: int, sensor_in: SensorUpdate, session: Session = Depends(get_db)
):
    # https://fastapi.tiangolo.com/tutorial/body-updates/#using-pydantics-exclude-unset-parameter
    sensor = session.get(Sensor, sensor_id)

    if not sensor:
        raise HTTPException(status_code=404, detail="Sensor not found.")

    update_data = sensor_in.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(sensor, key, value)

    session.commit()
    return sensor


@router.get("/{sensor_id}/readings", response_model=list[ReadingOut])
async def read_readings(sensor_id: int, session: Session = Depends(get_db)):
    sensor = session.get(Sensor, sensor_id)

    if not sensor:
        raise HTTPException(status_code=404, detail="Sensor not found.")

    return sensor.readings


@router.post("/{sensor_id}/readings", status_code=201, response_model=ReadingOut)
async def create_fake_reading(sensor_id: int, session: Session = Depends(get_db)):
    new_reading = Reading(
        sensor_id=sensor_id, humidity=randrange(20, 90), temperature=randrange(0, 50)
    )
    session.add(new_reading)
    session.commit()

    return new_reading
    # add status code to all endpoints
    # add docstrings to functions
