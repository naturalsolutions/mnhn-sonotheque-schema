MEDIA_KEYS_MAPPING_v1: dict = {
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
    "ESPECE_PK": "species_primary_key",
    "MIME_TYPE": "mime_type",
}

class ImportConversionMapper:
    def __init__(self, schema_version: int = 1):
        self.schema_version = schema_version

    def get_media_mapping(self) -> dict:
        """
    A dictionary mapping original column names to their new names for media data.

    This dictionary is used to standardize column names from various sources into a consistent format.
    The keys represent the original column names, and the values represent the new standardized column names.

    Example:
        {
            "SON_PK": "son_primary_key",
            "SON_UID": "code",
            "TYPE": "type",
            "TITRE": "title",
            ...
        }

    Attributes:
        SON_PK (str): Maps to "son_primary_key".
        SON_UID (str): Maps to "code".
        TYPE (str): Maps to "type".
        TITRE (str): Maps to "title".
        INSTITUTION_CODE (str): Maps to "institution_code".
        COLLECTION_CODE (str): Maps to "collection_code".
        CATALOG_NUMBER (str): Maps to "catalog_number".
        VALIDE (str): Maps to "valid".
        VALIDE_PAR (str): Maps to "validated_by".
        PUBLIE (str): Maps to "published".
        DATE_PUBLICATION_DEBUT (str): Maps to "publication_start_date".
        DATE_PUBLICATION_FIN (str): Maps to "publication_end_date".
        PUBLICATION_SCIENTIFIQUE (str): Maps to "scientific_publication".
        RECORDER (str): Maps to "recorder".
        MICRO (str): Maps to "micro".
        PARABOLE (str): Maps to "parabola".
        FREQUENCE_ECHANTILLONNAGE (str): Maps to "sampling_frequency".
        SUPPORT_ORIGINAL (str): Maps to "original_support".
        QUALITE (str): Maps to "quality".
        DATE_ENREGISTREMENT_INT (str): Maps to "registration_date_int".
        HEURE_ENREGISTREMENT_INT (str): Maps to "registration_time_int".
        LIEU_ENREGISTREMENT (str): Maps to "registration_place".
        TEMPERATURE (str): Maps to "temperature".
        COMMENTAIRES_ENREGISTREMENT (str): Maps to "registration_comments".
        CONTEXTE_COMPORTEMENTAL (str): Maps to "behavioral_context".
        HABITAT (str): Maps to "habitat".
        DESCRIPTION_HABITAT (str): Maps to "habitat_description".
        CONTINENT_OCEAN (str): Maps to "continent_ocean".
        PAYS (str): Maps to "country".
        LOCALITE (str): Maps to "locality".
        LATITUDE (str): Maps to "latitude".
        LONGITUDE (str): Maps to "longitude".
        ALTITUDE (str): Maps to "altitude".
        COMMENTAIRES (str): Maps to "comments".
        DATECRE (str): Maps to "creation_date".
        DATEMAJ (str): Maps to "last_modified_date".
        USERCRE (str): Maps to "created_by".
        USERMAJ (str): Maps to "modified_by".
        NOM_SCIENTIFIQUE (str): Maps to "scientific_name".
        ESPECE_PK (str): Maps to "species_primary_key".
        MIME_TYPE (str): Maps to "mime_type".
        """
        return MEDIA_KEYS_MAPPING_v1