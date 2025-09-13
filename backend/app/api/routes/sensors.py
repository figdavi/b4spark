from datetime import datetime
from random import randrange

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db import get_db
from app.models import (
    Reading,
    ReadingOut,
    Sensor,
    SensorCreate,
    SensorOut,
    SensorUpdate,
)

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
    """
    Retrieve sensors.
    """
    sensors = session.scalars(select(Sensor).order_by(Sensor.id)).all()

    return sensors


@router.post("/", status_code=201, response_model=SensorOut)
async def create_sensor(
    data: SensorCreate,
    session: Session = Depends(get_db),
):
    """
    Create a new sensor.
    """
    new_sensor = Sensor(**data.model_dump())

    session.add(new_sensor)
    session.commit()
    session.refresh(new_sensor)

    return new_sensor


@router.patch("/{sensor_id}", response_model=SensorOut)
async def update_sensor(
    sensor_id: int, sensor_in: SensorUpdate, session: Session = Depends(get_db)
):
    """
    Update properties of a sensor (Patch).
    """
    # https://fastapi.tiangolo.com/tutorial/body-updates/#using-pydantics-exclude-unset-parameter
    sensor = session.get(Sensor, sensor_id)

    if not sensor:
        raise HTTPException(status_code=404, detail="Sensor not found.")

    update_data = sensor_in.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(sensor, key, value)

    session.commit()
    session.refresh(sensor)

    return sensor


@router.get("/{sensor_id}/readings", response_model=list[ReadingOut])
async def read_sensor_readings(
    sensor_id: int,
    start_period: datetime | None = None,
    end_period: datetime | None = None,
    session: Session = Depends(get_db),
):
    """
    Retrieve readings by a sensor, optionally by a date range.
    """
    sensor = session.get(Sensor, sensor_id)

    if not sensor:
        raise HTTPException(status_code=404, detail="Sensor not found.")

    if start_period and end_period and start_period > end_period:
        raise HTTPException(
            status_code=400, detail="start_period must be less than end_period"
        )

    stmt = select(Reading).where(Reading.sensor_id == sensor_id)

    if start_period:
        stmt = stmt.where(Reading.read_at >= start_period)
    if end_period:
        stmt = stmt.where(Reading.read_at <= end_period)

    readings = session.scalars(stmt.order_by(Reading.read_at)).all()

    return readings


@router.post("/{sensor_id}/readings", status_code=201, response_model=ReadingOut)
async def create_fake_reading(sensor_id: int, session: Session = Depends(get_db)):
    """
    Create a new (fake) reading by a sensor.
    """
    new_reading = Reading(
        sensor_id=sensor_id, humidity=randrange(20, 90), temperature=randrange(0, 50)
    )
    session.add(new_reading)
    session.commit()
    session.refresh(new_reading)

    return new_reading
