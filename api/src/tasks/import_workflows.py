import uuid
import pandas as pd
from celery import shared_task
from src.schemas.media import MediaTypeEnum, MediaSubTypeEnum
# import dask.dataframe as dd
# from sqlalchemy import func

from src.utils.import_schema_converter import SchemaConverter
from sqlalchemy.orm import Session
from src.database import engine
import uuid


@shared_task(name="process_import_file_test")
def process_csv_file(
    file_path: str = "src/tmp/data/sonotheque1.csv", num_rows: int = 30000
):
    # Temp: Mannually map dates columns to datetime
    date_cols = [
        "DATECRE",
        "DATEMAJ",
        "DATE_PUBLICATION_DEBUT",
        "DATE_PUBLICATION_FIN",
        "DATEMAJ3",
        "DATEMAJ9",
        "DATEMAJ14",
        "DATEMAJ19",
        "DATEMAJ28",
        "DATEMAJ33",
        "DATEMAJ38",
        "DATEMAJ43",
        "DATEMAJ48",
        "DATEMAJ53",
        "DATEMAJ61",
        "DATEMAJ68",
        "DATEMAJ74",
        "DATEMAJ81",
        "DATECRE2",
        "DATECRE8",
        "DATECRE13",
        "DATECRE18",
        "DATECRE27",
        "DATECRE32",
        "DATECRE37",
        "DATECRE42",
        "DATECRE47",
        "DATECRE52",
        "DATECRE60",
        "DATECRE67",
        "DATECRE73",
        "DATECRE80",
    ]

    # # Read the CSV file into a Dask DataFrame
    # df = dd.read_csv(
    #     file_path,
    #     sep=";",
    #     quotechar='"',
    #     parse_dates=date_cols,
    #     sample=25000000,
    #     low_memory=False,  # Disable pandas' dtype inference
    # )

    # # Convert to Pandas DataFrame and select first num_rows
    # pdf = df.compute().head(num_rows)

    pdf = pd.read_csv(
        file_path,
        sep=";",
        nrows=num_rows,
        quotechar='"',
        parse_dates=date_cols,
        low_memory=False,
    )

    # Transformations operation through class converter
    converter = SchemaConverter(pdf, exclude_unmapped_initial_columns=False)
    converter.convert_schema()
    print(converter.df.head(10))
    medias_df = converter.aggregate_sounds()

    # Process the DataFrame
    for _, row in medias_df.iterrows():
        process_csv_row.delay(row.to_dict())
    return pdf.dtypes


@shared_task
def process_csv_row(row: dict):
    location_data = {
        "locality": row["locality"],
        "geom": set_geom(row),
        "identifier": str(uuid.uuid4()),
        # "geom": func.ST_SetSRID(
        #     func.ST_MakePoint(row["longitude"], row["latitude"]), 4326
        # ),
        # ... other location fields
    }

    media_data = {
        "title": row["title"],
        "subtype": row["type"],
        "comment": row["registration_comments"],
        "code": row["catalog_number"],
        "created_at": row["creation_date"],
        "updated_at": row["last_modified_date"],
        # ... other media fields
    }

    # Insert location
    location_id = get_or_insert_location(location_data)

    # Insert media with location_id
    media_id = get_or_insert_media(media_data, location_id)

    # return row
    return {"media_id": media_id, "location_id": location_id}


def set_geom(row: dict):
    if row["latitude"] and row["longitude"]:
        return f"POINT({row['latitude']} {row['longitude']})"
    return None


def get_or_insert_location(location_data: dict):
    from src.schemas.location import LocationCreate
    from src.models.locations import Location

    import datetime

    # Convert datetime objects to ISO format strings
    for key, value in location_data.items():
        if isinstance(value, datetime.datetime):
            location_data[key] = value.isoformat()

    required_fields = LocationCreate.model_fields.keys()
    for field in required_fields:
        if field not in location_data:
            location_data[field] = None
    location = LocationCreate(**location_data)

    with Session(engine) as session:
        existing_location = (
            session.query(Location).filter_by(locality=location.locality).first()
        )
        if existing_location:
            db_location = existing_location
        else:
            db_location = Location(**location.model_dump())
            session.add(db_location)
            session.commit()
            session.refresh(db_location)
    return db_location.id


def get_or_insert_media(media_data: dict, location_id: uuid.UUID = None):
    from src.schemas.media import MediaCreate
    from src.models.medias import Media
    import datetime

    # Convert datetime objects to ISO format strings
    for key, value in media_data.items():
        if isinstance(value, datetime.datetime):
            media_data[key] = value.isoformat()

    required_fields = MediaCreate.model_fields.keys()
    for field in required_fields:
        if field not in media_data:
            media_data[field] = None
    media = MediaCreate(**media_data)
    print(media)
    with Session(engine) as session:
        existing_media = session.query(Media).filter_by(code=media.code).first()
        if existing_media:
            db_media = existing_media
        else:
            db_media = Media(**media.model_dump())
            if location_id:
                db_media.location_id = location_id
            session.add(db_media)
            session.commit()
            session.refresh(db_media)
    return db_media.id
