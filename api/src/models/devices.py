from sqlalchemy import Column, Text
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
import uuid

from src.database import Base, DefaultColsMixin


class Device(DefaultColsMixin, Base):
    """
    Represents a device used for capturing media.

    This class inherits from DefaultColsMixin and Base, and defines the structure
    for the 'devices' table in the database.

    Attributes:
        id (UUID): Primary key, unique identifier for the device.
        brand (str): Brand of the capture device.
        model (str): Model of the capture device.
        firmware_version (str): Version of the firmware installed on the device during recording.
        type (str): Type of the capture device (e.g., Recorder, Microphone, Camera, Camera trap).
        media_files (relationship): Many-to-many relationship with MediaFile through the 'captures' association table.
    """

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

    # Relationships
    # many-to-many relationship to MediaFiles with a custom association table
    media_files = relationship(
        "MediaFile", secondary="captures", back_populates="devices"
    )
