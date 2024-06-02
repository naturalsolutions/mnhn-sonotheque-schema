from pydantic import BaseModel, Field
import uuid

from enum import Enum


class DeviceType(Enum):
    recorder = "Recorder"
    microphone = "Microphone"
    camera = "Camera"
    camera_trap = "CameraTrap"


class Device(BaseModel):
    id: uuid.UUID = Field(
        default_factory=uuid.uuid4, description="Brand of the capture device"
    )
    brand: str = Field(..., description="Brand of the capture device")
    model: str = Field(..., description="Model of the capture device")
    firmware_version: str = Field(
        ...,
        description="Version of the firmware installed on the device during recording",
    )
    type: str = Field(
        ...,
        description="Type of the capture device; e.g Recorder, Microphone, Camera, Camera trap",
    )

    class Config:
        from_attributes = True
