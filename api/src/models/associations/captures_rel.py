from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, relationship

from src.database import Base, DefaultColsMixin
from src.models.devices import Device
from src.models.media_files import MediaFile


class Captures(DefaultColsMixin, Base):
    __tablename__ = "captures"

    device_id = Column(
        UUID(as_uuid=True),
        ForeignKey("devices.id"),
        primary_key=True,
        comment="Device UUID",
    )
    media_file_id = Column(
        UUID(as_uuid=True),
        ForeignKey("media_files.id"),
        primary_key=True,
        comment="Media file UUID",
    )

    # Relationships
    device: Mapped["Device"] = relationship(back_populates="captures")
    media_file: Mapped["MediaFile"] = relationship(back_populates="captures")
