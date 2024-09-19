class SchemaConverter:
    """
    A class for converting and processing data schemas.

    This class is designed to convert data from one schema to another, specifically
    tailored for processing media-related data. It handles column mapping, data
    aggregation, and various transformations needed to align the input data with
    the target schema.

    Attributes:
        df (pandas.DataFrame): The input DataFrame to be converted.
        conversion_dict (dict): A dictionary mapping original column names to their new names.
        exclude_unmapped_initial_columns (bool): If True, columns not in the conversion_dict will be excluded.
        aggregated_sound_df (pandas.DataFrame): The resulting DataFrame after schema conversion and aggregation.

    Methods:
        convert_schema(): Performs the main schema conversion process.
        aggregate_sounds(): Aggregates sound data to extract media metadata.
        (Other methods may be present but are not visible in the provided snippet)

    The class is particularly useful for standardizing data from various sources
    into a consistent format, especially for media and sound-related information.
    """

    def __init__(self, df, exclude_unmapped_initial_columns=False):
        self.df = df
        self.conversion_dict = {
            "SON_PK": "son_primary_key",
            "SON_UID": "code",
            "TYPE": "type",
            "TITRE": "title",
            "INSTITUTION_CODE": "institution_code",
            "COLLECTION_CODE": "collection_code",
            "CATALOG_NUMBER": "catalog_number",
            "VALIDE": "valid",
            "VALIDE_PAR": "validated_by",
            "PUBLIE": "published",
            "DATE_PUBLICATION_DEBUT": "publication_start_date",
            "DATE_PUBLICATION_FIN": "publication_end_date",
            "PUBLICATION_SCIENTIFIQUE": "scientific_publication",
            "RECORDER": "recorder",
            "MICRO": "micro",
            "PARABOLE": "parabola",
            "FREQUENCE_ECHANTILLONNAGE": "sampling_frequency",
            "SUPPORT_ORIGINAL": "original_support",
            "QUALITE": "quality",
            "DATE_ENREGISTREMENT_INT": "registration_date_int",
            "HEURE_ENREGISTREMENT_INT": "registration_time_int",
            "LIEU_ENREGISTREMENT": "registration_place",
            "TEMPERATURE": "temperature",
            "COMMENTAIRES_ENREGISTREMENT": "registration_comments",
            "CONTEXTE_COMPORTEMENTAL": "behavioral_context",
            "HABITAT": "habitat",
            "DESCRIPTION_HABITAT": "habitat_description",
            "CONTINENT_OCEAN": "continent_ocean",
            "PAYS": "country",
            "LOCALITE": "locality",
            "LATITUDE": "latitude",
            "LONGITUDE": "longitude",
            "ALTITUDE": "altitude",
            "COMMENTAIRES": "comments",
            "DATECRE": "creation_date",
            "DATEMAJ": "last_modified_date",
            "USERCRE": "created_by",
            "USERMAJ": "modified_by",
            "NOM_SCIENTIFIQUE": "scientific_name",
            # Add more conversions as needed
        }
        self.exclude_unmapped_initial_columns = exclude_unmapped_initial_columns
        self.aggregated_sounds_df = None

    def convert_schema(self):
        custom_schema = {}
        for column in self.df.columns:
            custom_name = self.conversion_dict.get(
                column, column
            )  # Use original name if not found
            if custom_name != column:  # Only infclude mapped columns
                custom_schema[custom_name] = column
                self.df.rename(
                    columns={column: custom_name}, inplace=True
                )  # Rename columns in the original dataframe
            if self.exclude_unmapped_initial_columns:
                self.df = self.df[
                    self.df.columns.intersection(self.conversion_dict.values())
                ]
        return custom_schema

    def aggregate_sounds(self):
        import pandas as pd

        if "son_primary_key" not in self.df.columns:
            raise ValueError(
                "The 'son_primary_key' column is not present in the dataframe."
            )

        # Group by 'son_primary_key' and aggregate all other columns
        # legacy keep only first value
        # aggregated_df = self.df.groupby("son_primary_key").agg(lambda x: x.iloc[0])

        # We use 'first' to keep only the first value for each group
        aggregated_df = (
            self.df.groupby("son_primary_key")
            .agg(lambda x: x.tolist())
            .map(lambda x: list(set(x)))
            .map(lambda x: x[0] if len(x) == 1 else x)
            .map(
                lambda x: pd.NA
                if isinstance(x, list) and all(pd.isna(item) for item in x)
                else x
            )
        )

        # Reset the index to make 'son_primary_key' a regular column again
        aggregated_df = aggregated_df.reset_index()
        print(aggregated_df.head(10))

        # Update the dataframe in place
        self.aggregated_sounds_df = aggregated_df

        return self.aggregated_sounds_df
