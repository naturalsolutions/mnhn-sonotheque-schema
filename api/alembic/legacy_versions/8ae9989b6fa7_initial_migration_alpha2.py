"""Initial migration v2

Revision ID: 8ae9989b6fa7
Revises:
Create Date: 2024-08-04 08:48:56.100861

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
import geoalchemy2

# revision identifiers, used by Alembic.
revision: str = "8ae9989b6fa7"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "devices",
        sa.Column("id", sa.UUID(), nullable=False, comment="Identifier for the device"),
        sa.Column(
            "brand", sa.Text(), nullable=False, comment="Brand of the capture device"
        ),
        sa.Column(
            "model", sa.Text(), nullable=False, comment="Model of the capture device"
        ),
        sa.Column(
            "firmware_version",
            sa.Text(),
            nullable=False,
            comment="Version of the firmware installed on the device during recording",
        ),
        sa.Column(
            "type",
            sa.Text(),
            nullable=False,
            comment="Type of the capture device; e.g Recorder, Microphone, Camera, Camera trap",
        ),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "locations",
        sa.Column(
            "higher_geography_path",
            sa.String(),
            nullable=True,
            comment="Hierarchical path of geographic names less specific than locality",
        ),
        sa.Column(
            "geom",
            geoalchemy2.types.Geometry(
                srid=4326, from_text="ST_GeomFromEWKT", name="geometry"
            ),
            nullable=True,
            comment="Spatial geometry representing a location as WKB",
        ),
        sa.Column(
            "geometry_precision",
            sa.Float(),
            nullable=True,
            comment="Precision of the coordinates",
        ),
        sa.Column(
            "identifier",
            sa.String(),
            nullable=False,
            comment="Unique text identifier used in hierarchical path",
        ),
        sa.Column(
            "country",
            sa.String(),
            nullable=True,
            comment="Country or major administrative unit of the location",
        ),
        sa.Column(
            "state_province",
            sa.String(),
            nullable=True,
            comment="Administrative region smaller than country",
        ),
        sa.Column(
            "municipality",
            sa.String(),
            nullable=True,
            comment="Smaller administrative region than county",
        ),
        sa.Column(
            "locality",
            sa.String(),
            nullable=True,
            comment="Specific description of the place",
        ),
        sa.Column(
            "depth_min",
            sa.Float(),
            nullable=True,
            comment="Minimum depth below local surface in meters",
        ),
        sa.Column(
            "elevation_max",
            sa.Float(),
            nullable=True,
            comment="Maximum elevation above sea level in meters",
        ),
        sa.Column(
            "sampling_remarks",
            postgresql.JSONB(astext_type=sa.Text()),
            nullable=True,
            comment="Notes about the sampling location including meteorological context",
        ),
        sa.Column(
            "remarks",
            sa.String(),
            nullable=True,
            comment="General comments or notes about the location",
        ),
        sa.Column(
            "provided_id",
            sa.String(),
            nullable=True,
            comment="External ID from a service",
        ),
        sa.Column(
            "provider_source",
            sa.String(),
            nullable=True,
            comment="Source URL of the external service providing the ID",
        ),
        sa.Column(
            "parent_id",
            sa.UUID(),
            nullable=True,
            comment="Identifier for the parent location",
        ),
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(
            ["parent_id"],
            ["locations.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("identifier"),
    )
    op.create_index(
        "idx_locations_geom",
        "locations",
        ["geom"],
        unique=False,
        postgresql_using="gist",
    )
    op.create_table(
        "people",
        sa.Column("full_name", sa.String(), nullable=False),
        sa.Column("birth_date", sa.Date(), nullable=True),
        sa.Column("death_date", sa.Date(), nullable=True),
        sa.Column("has_gender", sa.String(), nullable=True),
        sa.Column("email", sa.String(), nullable=True),
        sa.Column("identity_provider", sa.String(), nullable=True),
        sa.Column("identity_token", sa.String(), nullable=True),
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "organizations",
        sa.Column(
            "parent_id",
            sa.UUID(),
            nullable=True,
            comment="FK to represent hierarchy in organization, e.g., main organizations and units",
        ),
        sa.Column(
            "name", sa.String(), nullable=False, comment="Name of the organizations"
        ),
        sa.Column(
            "type", sa.String(), nullable=False, comment="Category of the organization"
        ),
        sa.Column(
            "contact",
            sa.String(),
            nullable=True,
            comment="Free text form for contact information",
        ),
        sa.Column(
            "contact_id",
            sa.UUID(),
            nullable=True,
            comment="Foreign Key to the orgzanization contact; just one contact for a given organization in this version of the schema",
        ),
        sa.Column("location_id", sa.UUID(), nullable=True, comment="FK to location"),
        sa.Column(
            "description",
            sa.String(),
            nullable=True,
            comment="Description of the organization",
        ),
        sa.Column(
            "dynamic_properties",
            postgresql.JSONB(astext_type=sa.Text()),
            nullable=False,
            comment="Flexible JSON schema to store additional properties",
        ),
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(
            ["contact_id"],
            ["people.id"],
        ),
        sa.ForeignKeyConstraint(
            ["location_id"],
            ["locations.id"],
        ),
        sa.ForeignKeyConstraint(
            ["parent_id"],
            ["organizations.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "sampling_events",
        sa.Column(
            "parent_id",
            sa.UUID(),
            nullable=True,
            comment="An identifier for the broader dwc:Event that groups this and potentially other dwc:Events.",
        ),
        sa.Column(
            "basis_of_record",
            sa.ARRAY(sa.Text()),
            nullable=True,
            comment="Type of record collected in the sampling event: whether Human Observation or Machine Observation",
        ),
        sa.Column(
            "type",
            sa.Text(),
            nullable=True,
            comment="The nature of the dwc:Event. Recommended best practice is to use a controlled vocabulary.",
        ),
        sa.Column(
            "sampling_protocol",
            sa.Text(),
            nullable=True,
            comment="The names of, references to, or descriptions of the methods or protocols used during a dwc:Event.",
        ),
        sa.Column(
            "started_at",
            sa.TIMESTAMP(),
            nullable=True,
            comment="The date-time or interval during which a dwc:Event occurred",
        ),
        sa.Column(
            "ended_at",
            sa.TIMESTAMP(),
            nullable=True,
            comment="The date-time or interval during which a dwc:Event occurred",
        ),
        sa.Column(
            "date_range",
            sa.ARRAY(sa.TIMESTAMP()),
            nullable=True,
            comment="The date-time or interval during which a dwc:Event occurred",
        ),
        sa.Column(
            "habitat",
            sa.Text(),
            nullable=True,
            comment="A category or description of the habitat in which the dwc:Event occurred.",
        ),
        sa.Column(
            "notes",
            sa.Text(),
            nullable=True,
            comment="Comments or notes about the dwc:Event.",
        ),
        sa.Column(
            "measurements_or_facts",
            postgresql.JSONB(astext_type=sa.Text()),
            nullable=True,
            comment="A list (concatenated and separated) of additional measurements or characteristics of the Event.",
        ),
        sa.Column(
            "location_id",
            sa.UUID(),
            nullable=True,
            comment="Foreign Key to the location of the sampling event",
        ),
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(
            ["location_id"],
            ["locations.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "datasets",
        sa.Column(
            "id",
            sa.UUID(),
            server_default=sa.text("gen_random_uuid()"),
            nullable=False,
            comment="An identifier for the set of resources",
        ),
        sa.Column(
            "name",
            sa.String(),
            nullable=False,
            comment="The name identifying the data set from which the record was derived.",
        ),
        sa.Column(
            "description",
            sa.String(),
            nullable=False,
            comment="Description of the dataset",
        ),
        sa.Column(
            "doi",
            sa.String(),
            nullable=True,
            comment="Publication unique identifier for a reference associated to this datasets",
        ),
        sa.Column(
            "created_by",
            sa.UUID(),
            nullable=False,
            comment="Foreign Key to the dataset creator",
        ),
        sa.Column(
            "maintained_by",
            sa.UUID(),
            nullable=False,
            comment="Foreign Key to the dataset maintainers; just one maintainer for a given dataset in this version of the schema",
        ),
        sa.Column(
            "contact",
            sa.UUID(),
            nullable=False,
            comment="Foreign Key to the contact person for this dataset",
        ),
        sa.Column(
            "published_by",
            sa.UUID(),
            nullable=False,
            comment="Foreign Key to the organization",
        ),
        sa.Column(
            "created_at",
            sa.DateTime(),
            nullable=False,
            comment="Creation datetime for this resource",
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(),
            nullable=False,
            comment="Modification datetime for this resource",
        ),
        sa.Column(
            "dynamic_properties",
            postgresql.JSONB(astext_type=sa.Text()),
            nullable=False,
            comment="Flexible JSON schema to store additional properties",
        ),
        sa.ForeignKeyConstraint(
            ["contact"],
            ["people.id"],
        ),
        sa.ForeignKeyConstraint(
            ["created_by"],
            ["people.id"],
        ),
        sa.ForeignKeyConstraint(
            ["maintained_by"],
            ["people.id"],
        ),
        sa.ForeignKeyConstraint(
            ["published_by"],
            ["organizations.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_datasets_id"), "datasets", ["id"], unique=False)
    op.create_table(
        "media",
        sa.Column(
            "id",
            sa.UUID(),
            nullable=False,
            comment="Media identifier See: http://purl.org/dc/terms/identifier",
        ),
        sa.Column(
            "parent_id", sa.UUID(), nullable=True, comment="Parent media identifier"
        ),
        sa.Column(
            "code",
            sa.Text(),
            nullable=True,
            comment="A free-form identifier (a simple number, an alphanumeric code, a URL, etc.) for the resource that is unique and meaningful primarily for the data provider. See: http://rs.tdwg.org/ac/terms/providerManagedID",
        ),
        sa.Column(
            "title",
            sa.Text(),
            nullable=True,
            comment="Concise title, name, or brief descriptive label of institution, resource collection, or individual resource. This field SHOULD include the complete title with all the subtitles, if any. See: http://purl.org/dc/terms/title",
        ),
        sa.Column(
            "type",
            src.models.medias.MediaType(),
            nullable=True,
            comment="Type of media: Still Image, MovingImage, Sound See: http://purl.org/dc/terms/identifier",
        ),
        sa.Column(
            "subtype",
            src.models.medias.MediaSubtype(),
            nullable=True,
            comment="Subtype of media, e.g Species Sound, Soundscape, Song… (ideally should be linked to a Vocabulary terms should have an. IRI)",
        ),
        sa.Column(
            "description",
            sa.Text(),
            nullable=True,
            comment="An account of the resource. See: http://purl.org/dc/terms/description",
        ),
        sa.Column(
            "tags",
            sa.ARRAY(sa.Text()),
            nullable=True,
            comment="Media tags Tags may be multi-worded phrases. See: http://rs.tdwg.org/ac/terms/tag",
        ),
        sa.Column(
            "comment",
            sa.Text(),
            nullable=True,
            comment="Any comment provided on the media resource, as free-form text.",
        ),
        sa.Column(
            "resource_creation_technique",
            sa.Text(),
            nullable=True,
            comment="Information about technical aspects of the creation and digitization process of the resource. This includes modification steps ('retouching') after the initial resource capture. See: http://rs.tdwg.org/ac/terms/resourceCreationTechnique",
        ),
        sa.Column(
            "available",
            postgresql.DATERANGE(),
            nullable=True,
            comment="Date (often a range) that the resource became or will become available.",
        ),
        sa.Column(
            "created_at",
            sa.TIMESTAMP(),
            nullable=True,
            comment="Timestamp of resource creation in database",
        ),
        sa.Column(
            "updated_at",
            sa.TIMESTAMP(),
            nullable=True,
            comment="Timestamp of resource update in database See: http://purl.org/dc/terms/modified",
        ),
        sa.Column(
            "recorded_at",
            sa.TIMESTAMP(),
            nullable=True,
            comment="Timestamp of resource recording  The date and time MUST comply with the World Wide Web Consortium (W3C) datetime practice, https://www.w3.org/TR/NOTE-datetime See: http://ns.adobe.com/xap/1.0/CreateDate",
        ),
        sa.Column(
            "recording_range",
            postgresql.DATERANGE(),
            nullable=True,
            comment="Recording timestamp exact temporal coverage",
        ),
        sa.Column(
            "temporal",
            sa.Text(),
            nullable=True,
            comment="Temporal coverage of the resource See: http://purl.org/dc/terms/temporal",
        ),
        sa.Column(
            "time_of_day",
            sa.Text(),
            nullable=True,
            comment="Free text information beyond exact clock times. See: http://rs.tdwg.org/ac/terms/timeOfDay",
        ),
        sa.Column(
            "rating",
            sa.Integer(),
            nullable=True,
            comment="A user-assigned rating for the resource. The value shall be -1 or in the range [0..5], where -1 indicates 'rejected' and 0 indicates 'unrated'. If xmp:Rating is not present, a value of 0 should be assumed. See: http://ns.adobe.com/xap/1.0/Rating",
        ),
        sa.Column(
            "naturality_rating",
            sa.Integer(),
            nullable=True,
            comment="A user-assigned rating for perceived naturality. The value shall be -1 or in the range [0..5], where -1 indicates 'rejected' and 0 indicates 'unrated'. If xmp:Rating is not present, a value of 0 should be assumed. See: http://ns.adobe.com/xap/1.0/Rating",
        ),
        sa.Column(
            "musicality_rating",
            sa.Integer(),
            nullable=True,
            comment="A user-assigned rating for musical quality. The value shall be -1 or in the range [0..5], where -1 indicates 'rejected' and 0 indicates 'unrated'. If xmp:Rating is not present, a value of 0 should be assumed. See: http://ns.adobe.com/xap/1.0/Rating",
        ),
        sa.Column(
            "media_propagation", sa.Text(), nullable=True, comment="Location remarks"
        ),
        sa.Column(
            "ecological_tags",
            sa.ARRAY(sa.Text()),
            nullable=True,
            comment="Tags, eventually multi words, describing ecological and/or surrounding context ('audible river', 'biophonia',….)",
        ),
        sa.Column(
            "sampling_event_id",
            sa.UUID(),
            nullable=True,
            comment="Sampling event identifier",
        ),
        sa.Column(
            "created_by_id",
            sa.UUID(),
            nullable=True,
            comment="ID of the person who created the media",
        ),
        sa.Column(
            "updated_by_id",
            sa.UUID(),
            nullable=True,
            comment="ID of the person who last updated the media",
        ),
        sa.Column(
            "recorded_by_id",
            sa.UUID(),
            nullable=True,
            comment="ID of the person who recorded the media",
        ),
        sa.ForeignKeyConstraint(
            ["created_by_id"],
            ["people.id"],
        ),
        sa.ForeignKeyConstraint(
            ["recorded_by_id"],
            ["people.id"],
        ),
        sa.ForeignKeyConstraint(
            ["sampling_event_id"],
            ["sampling_events.id"],
        ),
        sa.ForeignKeyConstraint(
            ["updated_by_id"],
            ["people.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "media_files",
        sa.Column(
            "storage_url",
            sa.String(),
            nullable=True,
            comment="URL access point to the media",
        ),
        sa.Column(
            "mime_type_format",
            sa.String(),
            nullable=True,
            comment="Mimetype format of the file",
        ),
        sa.Column(
            "freq_low",
            sa.Float(),
            nullable=True,
            comment="The lowest frequency of the phenomena reflected in the multimedia item. Numeric value in hertz (Hz)",
        ),
        sa.Column(
            "freq_high",
            sa.Float(),
            nullable=True,
            comment="The highest frequency of the phenomena reflected in the multimedia item. Numeric value in hertz (Hz)",
        ),
        sa.Column(
            "sample_rate",
            sa.Float(),
            nullable=True,
            comment="Associates a digital signal to its sample rate. Numeric value in hertz (Hz)",
        ),
        sa.Column(
            "duration",
            sa.Integer(),
            nullable=True,
            comment="Duration of the media in seconds",
        ),
        sa.Column(
            "size", sa.Integer(), nullable=True, comment="Size of the media in bytes"
        ),
        sa.Column(
            "pixel_x_dimension",
            sa.Integer(),
            nullable=True,
            comment="Pixel X dimension",
        ),
        sa.Column(
            "pixel_y_dimension",
            sa.Integer(),
            nullable=True,
            comment="Pixel Y dimension",
        ),
        sa.Column(
            "creation_technique",
            sa.String(),
            nullable=True,
            comment="Information about technical aspects of the creation and digitization process of the resource",
        ),
        sa.Column(
            "rights",
            sa.String(),
            nullable=True,
            comment="Information about rights held in and over the resource",
        ),
        sa.Column(
            "attribution_url",
            sa.String(),
            nullable=True,
            comment="The URL where information about ownership, attribution, etc. of the resource may be found",
        ),
        sa.Column(
            "usage_terms",
            sa.String(),
            nullable=True,
            comment="A collection of text instructions on how a resource can be legally used",
        ),
        sa.Column(
            "cv_terms",
            postgresql.ARRAY(sa.String()),
            nullable=True,
            comment="A term to describe the content of the image by a value from a Controlled Vocabulary",
        ),
        sa.Column(
            "dynamic_metadata",
            postgresql.JSONB(astext_type=sa.Text()),
            nullable=True,
            comment="Any information that could be gathered from original file (XMP, IPTC, WAV header)",
        ),
        sa.Column(
            "owner_litteral",
            sa.String(),
            nullable=True,
            comment="Legal owner of the resource",
        ),
        sa.Column(
            "media_id", sa.UUID(), nullable=True, comment="Associated media UUID"
        ),
        sa.Column("owner_id", sa.UUID(), nullable=True, comment="Owner's UUID"),
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(
            ["media_id"],
            ["media.id"],
        ),
        sa.ForeignKeyConstraint(
            ["owner_id"],
            ["people.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("media_files")
    op.drop_table("media")
    op.drop_index(op.f("ix_datasets_id"), table_name="datasets")
    op.drop_table("datasets")
    op.drop_table("sampling_events")
    op.drop_table("organizations")
    op.drop_table("people")
    op.drop_index("idx_locations_geom", table_name="locations", postgresql_using="gist")
    op.drop_table("locations")
    op.drop_table("devices")
    # ### end Alembic commands ###
