from sqlalchemy import Column, String, Integer, Float, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, JSONB, ARRAY
from sqlalchemy.orm import Mapped, relationship

from typing import List

from api.src.database import Base, DefaultColsMixin
from src.devices.models import Device


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
        ForeignKey("devises.id"),
        primary_key=True,
        comment="Devise UUID",
    )
    extra_data = Column(JSONB, comment="Extra data for device-media association")

    # association between Assocation -> MediaFile
    media_file: Mapped["MediaFile"] = relationship(back_populates="device_associations")

    # association between Assocation -> Parent
    device: Mapped["Device"] = relationship(back_populates="media_file_associations")


class MediaFile(DefaultColsMixin, Base):
    __tablename__ = "media_files"

    storage_url = Column(String, comment="URL access point to the media")
    mime_type_format = Column(String, comment="Mimetype format of the file")
    freq_low = Column(
        Float,
        comment="The lowest frequency of the phenomena reflected in the multimedia item. Numeric value in hertz (Hz)",
    )
    freq_high = Column(
        Float,
        comment="The highest frequency of the phenomena reflected in the multimedia item. Numeric value in hertz (Hz)",
    )
    sample_rate = Column(
        Float,
        comment="Associates a digital signal to its sample rate. Numeric value in hertz (Hz)",
    )
    duration = Column(Integer, comment="Duration of the media in seconds")
    size = Column(Integer, comment="Size of the media in bytes")
    pixel_x_dimension = Column(Integer, comment="Pixel X dimension")
    pixel_y_dimension = Column(Integer, comment="Pixel Y dimension")
    creation_technique = Column(
        String,
        comment="Information about technical aspects of the creation and digitization process of the resource",
    )
    rights = Column(
        String, comment="Information about rights held in and over the resource"
    )
    attribution_url = Column(
        String,
        comment="The URL where information about ownership, attribution, etc. of the resource may be found",
    )
    usage_terms = Column(
        String,
        comment="A collection of text instructions on how a resource can be legally used",
    )
    cv_terms = Column(
        ARRAY(String),
        comment="A term to describe the content of the image by a value from a Controlled Vocabulary",
    )
    dynamic_metadata = Column(
        JSONB,
        comment="Any information that could be gathered from original file (XMP, IPTC, WAV header)",
    )
    owner_litteral = Column(String, comment="Legal owner of the resource")

    ### ForeignKeys ###
    media_id = Column(
        UUID(as_uuid=True), ForeignKey("media.id"), comment="Associated media UUID"
    )
    owner_id = Column(
        UUID(as_uuid=True), ForeignKey("people.id"), comment="Owner's UUID"
    )

    # many-to-many relationship to Device, bypassing the `Association` class
    devices: Mapped[List["Device"]] = relationship(
        secondary="media_files_to_devices_association", back_populates="media_files"
    )

    # association between MediaFile -> MediaFilesToDevicesAssociation -> Device
    device_associations: Mapped[List["MediaFilesToDevicesAssociation"]] = relationship(
        back_populates="media_file"
    )
