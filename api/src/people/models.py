from sqlalchemy import Column, String, Date
from sqlalchemy.orm import relationship

from src.database import Base, DefaultColsMixin


class Person(DefaultColsMixin, Base):
    __tablename__ = "people"

    full_name = Column(String, nullable=False)
    birth_date = Column(Date)
    death_date = Column(Date)
    has_gender = Column(String)
    email = Column(String)
    identity_provider = Column(String)
    identity_token = Column(String)

    ### ForeignKeys ###

    created_datasets = relationship(
        "Dataset", foreign_keys="Dataset.created_by", back_populates="creator"
    )
    maintained_datasets = relationship(
        "Dataset", foreign_keys="Dataset.maintained_by", back_populates="maintainer"
    )

    ### Relationships with backref ###
    created_medias = relationship("Media", backref="creator")
    edited_medias = relationship("Media", backref="editor")
    recorded_medias = relationship("Media", backref="recorder")
    owned_media_files = relationship("MediaFile", backref="owner")
