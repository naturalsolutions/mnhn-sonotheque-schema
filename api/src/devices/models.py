from sqlalchemy import Column, Text
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy.dialects.postgresql import UUID
from typing import List
import uuid

from src.database import Base, DefaultColsMixin
from src.devices.schemas import DeviceType


class Device(DefaultColsMixin, Base):
    __tablename__ = "devices"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        comment="Identifier for the device",
    )
    brand = Column(Text, nullable=False, comment="Brand of the capture device")
    model = Column(Text, nullable=False, comment="Model of the capture device")
    firmware_version = Column(
        Text,
        nullable=False,
        comment="Version of the firmware installed on the device during recording",
    )
    type = Column(
        Text,
        nullable=False,
        comment="Type of the capture device; e.g Recorder, Microphone, Camera, Camera trap",
    )

    # many-to-many relationship to MediaFiles, bypassing the `MediaFilesToDevicesAssociation` class
    media_files: Mapped[List["Device"]] = relationship(
        secondary="media_files_to_devices_association", back_populates="devices"
    )

    # association between Device -> MediaFilesToDevicesAssociation -> MediaFile
    media_file_associations: Mapped[List["MediaFilesToDevicesAssociation"]] = (
        relationship(back_populates="device")
    )
