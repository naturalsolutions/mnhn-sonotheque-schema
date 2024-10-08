from datetime import datetime
from uuid import uuid4
import pandas as pd
from pygbif import species
import re
from src.schemas.taxon import TaxonInDB


def camel_to_snake(string: str) -> str:
    """
    Convert a camelCase string to snake_case.

    Args:
        string (str): The camelCase string to convert.

    Returns:
        str: The converted snake_case string.
    """
    pattern = re.compile(r"(?<!^)(?=[A-Z])")
    return pattern.sub("_", string).lower()


def convert_dict_keys_to_snake_case(data: dict) -> dict:
    """
    Convert all keys in a dictionary from camelCase to snake_case.

    Args:
        data (dict): The dictionary with camelCase keys.

    Returns:
        dict: A new dictionary with all keys converted to snake_case.
    """
    return {camel_to_snake(key): value for key, value in data.items()}


def fetch_gbif_result(name: str) -> TaxonInDB | None:
    """
    Fetch a single result from GBIF for a given record.
    """

    try:
        result = species.name_backbone(name=name)
        if result:
            for entry in result:
                # Extract relevant fields from the entry
                new_entry = convert_dict_keys_to_snake_case(entry)
                taxon_default = TaxonInDB(
                    id=uuid4(),
                    created_at=datetime.now(),
                    updated_at=datetime.now(),
                )
                merged_data = taxon_default.model_dump()
                merged_data.update(new_entry)
                # result_data = {
                #     "sonotheque_scientific_name": name,
                #     "key": entry.get("key"),
                #     "name_key": entry.get("nameKey"),
                #     "vernacular_name": entry.get("vernacularNames"),
                #     "kingdom": entry.get("kingdom"),
                #     "phylum": entry.get("phylum"),
                #     "class": entry.get("class"),
                #     "order": entry.get("order"),
                #     "family": entry.get("family"),
                #     "genus": entry.get("genus"),
                #     "species": entry.get("species"),
                #     "scientific_name": entry.get("scientificName"),
                #     "canonical_name": entry.get("canonicalName"),
                #     "vernacular_name_original": entry.get(
                #         "vernacularNamesOriginal"
                #     ),
                #     "vernacular_name_english": entry.get("vernacularNamesEnglish"),
                #     "vernacular_name_french": entry.get("vernacularNamesFrench"),
                #     "rank": entry.get("rank"),
                #     "status": entry.get("status"),
                #     "synonym": entry.get("synonym"),
                # }
            return TaxonInDB(**merged_data).model_dump()
        else:
            return None
    except Exception as e:
        print(f"Error fetching data for {name}: {e}")
        return None
    pass


def fetch_gbif_results(names_list):
    """
    WARNING: deprecated method, use fetch_gbif_result() instead for parallel processing and idempotency
    Fetch results from GBIF for each name in the list and create a pandas DataFrame.

    Parameters:
    names_list (list): A list of scientific names to search in GBIF.

    Returns:
    pd.DataFrame: A DataFrame containing the results from GBIF.
    """
    results = []

    for name in names_list:
        try:
            result = species.name_suggest(q=name)
            if result:
                for entry in result:
                    # Extract relevant fields from the entry
                    result_data = {
                        "sonotheque_scientific_name": name,
                        "key": entry.get("key"),
                        "name_key": entry.get("nameKey"),
                        "vernacular_name": entry.get("vernacularNames"),
                        "kingdom": entry.get("kingdom"),
                        "phylum": entry.get("phylum"),
                        "class": entry.get("class"),
                        "order": entry.get("order"),
                        "family": entry.get("family"),
                        "genus": entry.get("genus"),
                        "species": entry.get("species"),
                        "scientific_name": entry.get("scientificName"),
                        "canonical_name": entry.get("canonicalName"),
                        "vernacular_name_original": entry.get(
                            "vernacularNamesOriginal"
                        ),
                        "vernacular_name_english": entry.get("vernacularNamesEnglish"),
                        "vernacular_name_french": entry.get("vernacularNamesFrench"),
                        "rank": entry.get("rank"),
                        "status": entry.get("status"),
                        "synonym": entry.get("synonym"),
                    }
                    results.append(result_data)
        except Exception as e:
            print(f"Error fetching data for {name}: {e}")

    # Convert the list of dictionaries to a DataFrame
    df_results = pd.DataFrame(results)
    return df_results
