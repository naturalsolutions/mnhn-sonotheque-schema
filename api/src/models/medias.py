from sqlalchemy import (
    Column,
    Enum,
    ForeignKey,
    Integer,
    Text,
    ARRAY,
    TIMESTAMP,
    UUID,
)
from sqlalchemy.dialects.postgresql import DATERANGE
import uuid
from sqlalchemy.orm import relationship
from src.database import DefaultColsMixin
from src.database import Base


class MediaType(Enum):
    image = "StillImage"
    sound = "Sound"
    video = "MovingImage"


class MediaSubtype(Enum):
    species_sound = "SpeciesSound"
    soundscape = "Soundscape"
    song = "Song"


class Media(DefaultColsMixin, Base):
    __tablename__ = "media"
    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        comment="Media identifier See: http://purl.org/dc/terms/identifier",
    )
    parent_id = Column(UUID(as_uuid=True), comment="Parent media identifier")
    code = Column(
        Text,
        comment="A free-form identifier (a simple number, an alphanumeric code, a URL, etc.) for the resource that is unique and meaningful primarily for the data provider. See: http://rs.tdwg.org/ac/terms/providerManagedID",
    )
    title = Column(
        Text,
        comment="Concise title, name, or brief descriptive label of institution, resource collection, or individual resource. This field SHOULD include the complete title with all the subtitles, if any. See: http://purl.org/dc/terms/title",
    )
    type = Column(
        MediaType,
        comment="Type of media: Still Image, MovingImage, Sound See: http://purl.org/dc/terms/identifier",
    )
    subtype = Column(
        MediaSubtype,
        comment="Subtype of media, e.g Species Sound, Soundscape, Song… (ideally should be linked to a Vocabulary terms should have an. IRI)",
    )
    description = Column(
        Text,
        comment="An account of the resource. See: http://purl.org/dc/terms/description",
    )
    tags = Column(
        ARRAY(Text),
        comment="Media tags Tags may be multi-worded phrases. See: http://rs.tdwg.org/ac/terms/tag",
    )
    comment = Column(
        Text, comment="Any comment provided on the media resource, as free-form text."
    )
    resource_creation_technique = Column(
        Text,
        comment="Information about technical aspects of the creation and digitization process of the resource. This includes modification steps ('retouching') after the initial resource capture. See: http://rs.tdwg.org/ac/terms/resourceCreationTechnique",
    )
    available = Column(
        DATERANGE,
        comment="Date (often a range) that the resource became or will become available.",
    )
    created_at = Column(TIMESTAMP, comment="Timestamp of resource creation in database")
    updated_at = Column(
        TIMESTAMP,
        comment="Timestamp of resource update in database See: http://purl.org/dc/terms/modified",
    )
    recorded_at = Column(
        TIMESTAMP,
        comment="Timestamp of resource recording  The date and time MUST comply with the World Wide Web Consortium (W3C) datetime practice, https://www.w3.org/TR/NOTE-datetime See: http://ns.adobe.com/xap/1.0/CreateDate",
    )
    recording_range = Column(
        DATERANGE, comment="Recording timestamp exact temporal coverage"
    )
    temporal = Column(
        Text,
        comment="Temporal coverage of the resource See: http://purl.org/dc/terms/temporal",
    )
    time_of_day = Column(
        Text,
        comment="Free text information beyond exact clock times. See: http://rs.tdwg.org/ac/terms/timeOfDay",
    )
    rating = Column(
        Integer,
        comment="A user-assigned rating for the resource. The value shall be -1 or in the range [0..5], where -1 indicates 'rejected' and 0 indicates 'unrated'. If xmp:Rating is not present, a value of 0 should be assumed. See: http://ns.adobe.com/xap/1.0/Rating",
    )
    naturality_rating = Column(
        Integer,
        comment="A user-assigned rating for perceived naturality. The value shall be -1 or in the range [0..5], where -1 indicates 'rejected' and 0 indicates 'unrated'. If xmp:Rating is not present, a value of 0 should be assumed. See: http://ns.adobe.com/xap/1.0/Rating",
    )
    musicality_rating = Column(
        Integer,
        comment="A user-assigned rating for musical quality. The value shall be -1 or in the range [0..5], where -1 indicates 'rejected' and 0 indicates 'unrated'. If xmp:Rating is not present, a value of 0 should be assumed. See: http://ns.adobe.com/xap/1.0/Rating",
    )
    media_propagation = Column(Text, comment="Location remarks")
    ecological_tags = Column(
        ARRAY(Text),
        comment="Tags, eventually multi words, describing ecological and/or surrounding context ('audible river', 'biophonia',….)",
    )

    ### ForeignKeys ###
    sampling_event_id = Column(
        UUID(as_uuid=True),
        ForeignKey("sampling_events.id"),
        nullable=True,
        comment="Sampling event identifier",
    )
    created_by_id = Column(
        UUID(as_uuid=True),
        ForeignKey("people.id"),
        nullable=True,
        comment="ID of the person who created the media",
    )
    updated_by_id = Column(
        UUID(as_uuid=True),
        ForeignKey("people.id"),
        nullable=True,
        comment="ID of the person who last updated the media",
    )
    recorded_by_id = Column(
        UUID(as_uuid=True),
        ForeignKey("people.id"),
        nullable=True,
        comment="ID of the person who recorded the media",
    )

    ### Relationships with backref ###
    media_files = relationship("MediaFile", backref="media")
    parent = relationship("Media", remote_side=[id], backref="children")
    # Relationships with backpopulates
    location = relationship("Location", back_populates="media")  # occurs in
    acoustic_events = relationship("AcousticEvent", back_populates="media")  # contains
    occurrences = relationship("Occurrence", back_populates="media")  # has
