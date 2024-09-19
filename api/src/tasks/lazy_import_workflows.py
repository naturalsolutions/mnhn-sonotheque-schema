import polars as pl
import pandas as pd
import patito as pt
from uuid import uuid4
from src.schemas.etl_data_models.media import Media
from celery import shared_task, chain, group
from celery.utils.log import get_task_logger
import base64
import os
import io



from src.utils.lazy_import_constructs import ImportConversionMapper


@shared_task(name="lazy_process_import_file")
def lazy_process_import_file(file_path: str = "src/tmp/data/sonotheque1.csv", num_rows: int = 10000):
    logger = get_task_logger(__name__)
    media_conversion_mapper = ImportConversionMapper(schema_version=1).get_media_mapping()
    # Scan the CSV file with Polars
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"The file at path {file_path} does not exist.")
    lf = pl.scan_csv(file_path, separator=";", infer_schema_length=None)
    # Rename columns using the conversion dictionary and remove columns not listed in the dictionary
    lf = lf.rename(media_conversion_mapper).select([pl.col(new_name) for new_name in media_conversion_mapper.values()])
    # Convert "last_modified_date" and "creation_date" columns to Polars temporal Datetime format
    lf = lf.with_columns([
        pl.col("last_modified_date").str.strptime(pl.Datetime, "%Y-%m-%d %H:%M:%S%.3f").alias("updated_at"),
        pl.col("creation_date").str.strptime(pl.Datetime, "%Y-%m-%d %H:%M:%S%.3f").alias("created_at"),
        pl.col("son_primary_key").map_elements(lambda _: str(uuid4())).alias("id"),
        # pl.col("mime_type").cast(pl.Categorical),
        # pl.col("type").cast(pl.Categorical)
    ])

    # Aggregate lf on son_primary_key and retain only the first occurrence of each value for all other columns
    aggregated_lf = lf.group_by("son_primary_key").agg(
        [pl.col(column).first().alias(column) for column in lf.columns if column != "son_primary_key"]
    )

    medias = pt.DataFrame(aggregated_lf.collect()).set_model(Media).drop().fill_null(strategy="defaults")
    logger.info(medias.head(10))

    logger.info("Loading media in DB")
    try:
        medias.write_database(table_name="media", connection=os.getenv("DATABASE_URL"), if_table_exists="append")
    except Exception as e:
        logger.error(f"Error writing to database: {e}")
    logger.info("Medias have been loaded in DB")
    
    
    # Create a LazyFrame that aggregates based on the scientific_name column
    taxon_lf = lf.group_by("scientific_name").agg(
        pl.col("species_primary_key").alias("species_primary_keys")
    )

    # Collect the LazyFrame into a DataFrame
    taxon_df = taxon_lf.collect()


    # # Serialize each row to Arrow IPC format and create tasks
    # taxon_tasks = []
    # for row in taxon_df.iter_rows(named=True):
    #     buffer = io.BytesIO()
    #     pl.DataFrame([row]).write_ipc(buffer)
    #     buffer.seek(0)
    #     ipc_data = base64.b64encode(buffer.getvalue()).decode('utf-8')
    #     taxon_tasks.append(process_taxon_checklist_record.s(ipc_data))

    # # Create a group of process_taxon_checklist_record tasks
    # taxon_group = group(taxon_tasks)



    
    # Collect the first N rows into a DataFrame
    # df = lf.collect().head(50)
    # print(f"df type: {type(df)}, value: {df}")
    # Create a group of process_row tasks
    # media_group = group(process_row.s(row) for row in df.iter_rows(named=True))

      # Collect the first N rows into a DataFrame
    # taxon_df = taxon_lf.collect().head(50)
    # print(f"df type: {type(df)}, value: {df}")
    # Create a group of process_row tasks
    # taxon_group = group(process_taxon_record.s(row) for row in taxon_df.iter_rows(named=True))
    
    # # Chain the tasks and set lazy_process_import_file as successful when all process_row tasks are done
    # chain(tasks)()
    # Chain the taxon_tasks and tasks, and set lazy_process_import_file as successful when all tasks are done
    
    # chain(media_group, taxon_group)()


# Update the process_taxon_checklist_record function
    
@shared_task(name="process_taxon_checklist_record")
def process_taxon_checklist_record(ipc_data: str):
        logger = get_task_logger(__name__)
        
        # Decode the base64 string and create a BytesIO object
        ipc_buffer = io.BytesIO(base64.b64decode(ipc_data))
        
        # Read the IPC format data into a Polars DataFrame
        df = pl.read_ipc(ipc_buffer)
        
        # Process the single row in the DataFrame
        for row in df.iter_rows(named=True):
            logger.info(f"Processing taxon: {row['scientific_name']}")
            logger.info(f"Species primary keys: {row['species_primary_keys']}")
            # Add your processing logic here
            # For example:
            # process_taxon(row['scientific_name'], row['species_primary_keys'])
        
        return f"Processed taxon: {row['scientific_name']}"

@shared_task(name="process_taxon_checklist")
def process_taxon_checklist(ipc_data: str):
    logger = get_task_logger(__name__)
    
    # Decode the base64 string and deserialize the Arrow IPC format to a Polars DataFrame
    df = pl.read_ipc(base64.b64decode(ipc_data))
    
    # Process each row
    for row in df.iter_rows(named=True):
        logger.info(row)
        # Process the row as needed
        # ...
    
    return "Processed"

@shared_task(name="process_taxon_record")
def process_taxon_record(list_of_media_rows, row: dict):
    logger = get_task_logger(__name__)
    logger.info(len(list_of_media_rows))
    logger.info(row)
    return row
    pass

@shared_task(name="lazy_process_row")
def process_row(row: dict):
    logger = get_task_logger(__name__)
    logger.info(row)
    return row
    pass