import duckdb
import ibis
from ibis import _
import pandas as pd
from uuid import uuid4
from src.utils.gbif import fetch_gbif_result
from src.schemas.etl_data_models.media import Media
from src.schemas.taxon import TaxonInDB
from celery import shared_task, chain, group, chord
from celery.utils.log import get_task_logger
import base64
import os
import io


from src.utils.lazy_import_constructs import ImportConversionMapper


@shared_task(name="mds_process_csv_file")
def mds_process_csv_file(
    file_path: str = "src/tmp/data/sonotheque1.csv", num_rows: int = 10000
):
    logger = get_task_logger(__name__)
    # preparation_chain = prepare_duckdb_persistance.s("sonotheque.duckdb") | create_import_records_table.s(file_path) | show_tables.s() | insert_defaut_items.s() | insert_taxa_checklist.s()
    # preparation_chain()
    res = chain(
        prepare_duckdb_persistance.s("sonotheque.duckdb"),
        create_import_records_table.s(file_path),
        show_tables.s(),
        add_uuids_to_sounds_records.s(),
        insert_defaut_items.s(),
        insert_taxa_checklist.s(),
    )()
    df_length = res.get()
    logger.info(f"df_length: {df_length}")


@shared_task(name="prepare-duckdb-persistance")
def prepare_duckdb_persistance(db_name: str = "sonotheque.duckdb") -> str:
    """
    Prepare a DuckDB database file for persistence.

    This task checks if a DuckDB database file exists at the specified path. If it doesn't exist,
    it creates an empty DuckDB file. This ensures that we have a valid DuckDB file to work with
    in subsequent tasks.

    Args:
        db_name (str): The name of the DuckDB database file. Defaults to "sonotheque.duckdb".

    Returns:
        str: The full path to the DuckDB database file.

    Raises:
        None

    Note:
        The database file is created in the 'src/tmp/db/' directory.
    """
    logger = get_task_logger(__name__)
    # Check if the file exists, if not, create it
    db_path = f"src/tmp/db/{db_name}"
    if not os.path.exists(db_path):
        # Create an empty DuckDB file
        duckdb.connect(db_path).close()
        logger.info("Created sonotheque.duckdb file.")
    else:
        logger.info(f"{db_name} file already exists.")
    return db_path


@shared_task(name="create-import-records-table")
def create_import_records_table(db_path: str, csv_file_path: str) -> str:
    logger = get_task_logger(__name__)
    con = duckdb.connect(db_path)
    try:
        # Create a table named 'import_records' from the CSV file
        con.execute(
            f"""
            CREATE TABLE IF NOT EXISTS import_records AS
            SELECT * FROM read_csv('{csv_file_path}', header=True, delim=';')
        """
        )
        logger.info(f"Successfully created 'import_records' table from {csv_file_path}")
    except Exception as e:
        logger.error(f"Error creating 'import_records' table: {str(e)}")
        raise
    finally:
        con.close()
        return db_path


@shared_task(name="show-tables")
def show_tables(db_path) -> str:
    logger = get_task_logger(__name__)
    # List DuckDB tables
    logger.info("Listing DuckDB tables:")
    try:
        logger.info("Connecting to DuckDB database")
        ddb_con = duckdb.connect("src/tmp/db/sonotheque.duckdb")
    except Exception as e:
        logger.error(f"Failed to connect to DuckDB: {str(e)}")
        raise
    finally:
        tables = ddb_con.sql("SHOW TABLES").fetchall()
        for table in tables:
            logger.info(f"- {table[0]}")
        ddb_con.close()
        logger.info("DuckDB connection closed.")
        return db_path


@shared_task(name="add-uuids-to-sounds-records")
def add_uuids_to_sounds_records(db_path) -> str:
    logger = get_task_logger(__name__)
    con = duckdb.connect(db_path)
    try:
        logger.info(
            "Add a UUID column to records and generate a UUID for each unique SON_UID value"
        )
        # Check if record_uuid column already exists
        columns = con.sql("PRAGMA table_info(import_records)").df()
        if "record_uuid" not in columns["name"].values:
            ### SQL Queries ##
            add_record_uuid_query = """
            --beginsql
            ALTER TABLE import_records
            ADD COLUMN record_uuid UUID;
            --endsql
            """

            # Generate and assign UUIDs for each unique SON_UID
            generate_and_assign_uuids_query = """
            --beginsql
            WITH unique_son_uids AS (
                    SELECT DISTINCT SON_UID
                FROM import_records
            ),
            uuid_mapping AS (
                SELECT
                    SON_UID,
                    uuid() AS new_uuid
                FROM unique_son_uids
            )
            UPDATE import_records
            SET record_uuid = uuid_mapping.new_uuid
            FROM uuid_mapping
                WHERE import_records.SON_UID = uuid_mapping.SON_UID;
            --endsql
            """
            # Add the record_uuid column to the import_records table
            verify_sound_uuids_query = """
            --beginsql
                    SELECT
                        record_uuid,
                        SON_UID,
                        NOM_SCIENTIFIQUE,
                        COUNT(*) OVER (PARTITION BY SON_UID) as records_per_son_uid
                    FROM import_records
                    ORDER BY SON_UID
                    LIMIT 10
            --endsql
            """

            con.sql(add_record_uuid_query)
            logger.info("Added record_uuid column to import_records table")
            logger.info("Generate and assign UUIDs for each unique SON_UID")
            con.sql(generate_and_assign_uuids_query)
            logger.info("Verify the new column and data")
            logger.info("Sample of records with new UUID column:")
            con.sql(verify_sound_uuids_query).show()
        else:
            logger.info("record_uuid column already exists in import_records table")
    except Exception as e:
        logger.error(f"Failed to add UUID column: {str(e)}")
        raise
    finally:
        con.close()
        return db_path


@shared_task(name="insert-default-items")
def insert_defaut_items(db_path) -> str:
    logger = get_task_logger(__name__)
    # Defaut Organization
    logger.info("TODO: Inserting default organization")
    # Default MainUser
    logger.info("TODO: Inserting default main user")
    # Default Dataset
    logger.info("TODO: Inserting default dataset")
    # Default Collection
    logger.info("TODO: Inserting default collection")
    return db_path


@shared_task(name="insert-taxa-checklist")
def insert_taxa_checklist(db_path) -> str:
    logger = get_task_logger(__name__)
    aggregate_taxa_query = """
    -- aggregation to get a list of taxa with their SON_UIDs and COLLECTION_CODE
    --beginsql
    SELECT
        uuid() AS UUID,
        NOM_SCIENTIFIQUE,
        LIST(SON_UID) AS SON_UIDS,
        FIRST(COLLECTION_CODE) AS COLLECTION_CODE
    FROM import_records
    GROUP BY NOM_SCIENTIFIQUE;
    --endsql
    """

    try:
        con = duckdb.connect(db_path)
        # results_df = con.sql(aggregate_taxa_query).df()
        # results = con.sql(aggregate_taxa_query).fetchall()

        # for row in results:
        #     fetch_taxa_gbif_data.s(row).apply_async()
        # logger.info(f"Results: {results_df.head()}")
        # con.close()
        # return len(results_df)
        callback = merge_gbif_result.s()
        header = [
            fetch_taxa_gbif_data.s(row)
            for row in con.sql(aggregate_taxa_query).fetchall()
        ]
        result = chord(header)(callback)
        result.get()
        con.close()
        return len(result)
    except Exception as e:
        logger.error(f"Failed to connect to DuckDB: {str(e)}")
        raise


GBIF_INDEX_SCIENTIFIC_NAME = 1


@shared_task(name="fetch-taxa-gbif-data")
def fetch_taxa_gbif_data(row: list) -> TaxonInDB:
    # import time
    # import random
    logger = get_task_logger(__name__)
    # Add a random sleep between 100ms and 1 second
    # sleep_time = random.uniform(0.1, 1)
    # logger.info(f"Sleeping for {sleep_time:.2f} seconds")
    # time.sleep(sleep_time)
    # logger.info(f"Type of row: {type(row)}")
    # logger.info(f"Row content: {row}")
    # return row
    scientific_name = row[GBIF_INDEX_SCIENTIFIC_NAME]
    logger.info(f"scientific_name: {scientific_name}")
    taxon = fetch_gbif_result(scientific_name)
    logger.info(f"taxon: {taxon}")
    return taxon


@shared_task(name="merge-gbif-result")
def merge_gbif_result(rows) -> str:
    logger = get_task_logger(__name__)
    try:
        # Create a DataFrame from the list of dictionaries
        df = pd.DataFrame(rows)
        logger.info(f"Created DataFrame with shape: {df.shape}")
        logger.info(f"DataFrame columns: {df.columns}")

        # Log a sample of the data (first few rows)
        logger.info(f"Sample data:\n{df.head()}")

        return len(df)
    except Exception as e:
        logger.error(f"Failed to create DataFrame: {str(e)}")
        raise
    pass
