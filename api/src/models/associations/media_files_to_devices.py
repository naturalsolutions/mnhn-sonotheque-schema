from sqlalchemy import Column, String, Integer, Float, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import Mapped, relationship

from typing import List

from src.database import Base, DefaultColsMixin
from src.devices.models import Device
from src.media_files.models import MediaFile


class MediaFilesToDevicesAssociation(DefaultColsMixin, Base):
    __tablename__ = "media_files_to_devices_association"
    media_file_id = Column(
        UUID(as_uuid=True),
        ForeignKey("media_files.id"),
        primary_key=True,
        comment="Media file UUID",
    )
    device_id = Column(
        UUID(as_uuid=True),
        ForeignKey("devices.id"),
        primary_key=True,
        comment="Device UUID",
    )
    extra_data = Column(JSONB, comment="Extra data for device-media association")

    # association between Assocation -> MediaFile
    media_file: Mapped["MediaFile"] = relationship(back_populates="device_associations")

    # association between Assocation -> Parent
    device: Mapped["Device"] = relationship(back_populates="media_file_associations")
