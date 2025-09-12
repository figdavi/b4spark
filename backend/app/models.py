from sqlalchemy import String, Float, DateTime, ForeignKey, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

# https://github.com/fastapi/full-stack-fastapi-template/blob/master/backend/app/models.py


class Base(DeclarativeBase):
    pass


class Sensor(Base):
    __tablename__ = "sensor"

    # Migrate to UUID, if needed
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    chip_id: Mapped[str] = mapped_column(
        String(20), nullable=False, index=True, unique=True
    )
    # Autogenerate friendly name, then make it editable
    friendly_name: Mapped[str] = mapped_column(String(50), nullable=False)
    latitude: Mapped[float] = mapped_column(Float, nullable=True)
    longitude: Mapped[float] = mapped_column(Float, nullable=True)
    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )

    measurements: Mapped[list["Measurement"]] = relationship(back_populates="sensor")


class Measurement(Base):
    __tablename__ = "measurements"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    sensor_id: Mapped[str] = mapped_column(ForeignKey("sensor.id"), nullable=False)
    humidity: Mapped[float] = mapped_column(Float, nullable=True)
    temperature: Mapped[float] = mapped_column(Float, nullable=True)
    measured_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )

    sensor: Mapped["Sensor"] = relationship(back_populates="measurements")
