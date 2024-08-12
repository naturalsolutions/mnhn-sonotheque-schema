from sqlalchemy import Column, UUID, DateTime, String, Float, JSON, func
from sqlalchemy.orm import declarative_base, relationship


from src.database import Base


class AcousticEvent(Base):
    __tablename__ = "acoustic_events"

    id = Column(UUID, primary_key=True)
    type = Column(String)
    region_of_interest = Column(JSON)
    time_end = Column(Float)
    time_start = Column(Float)
    x_frac = Column(Float)
    y_frac = Column(Float)
    width_frac = Column(Float)

    # Timestamps
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    # Foreign keys
    is_roi_of = Column(UUID)
    identification_id = Column(UUID)
    occurrence_id = Column(UUID)

    # Relationships with backpopulates
    media = relationship("Media", back_populates="acoustic_events")
    occurrences = relationship("Occurrence", back_populates="acoustic_event")
