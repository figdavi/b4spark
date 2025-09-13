from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.models import Sensor, SensorCreate, SensorOut, SensorUpdate
from app.db import get_db

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
        raise HTTPException(status_code=404, detail="Sensor not found")

    update_data = sensor_in.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(sensor, key, value)

    session.commit()
    return sensor
