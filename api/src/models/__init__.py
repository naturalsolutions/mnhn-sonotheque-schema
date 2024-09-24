"""
This module initializes and imports all the SQLAlchemy models used in the application.

The models included are:
- datasets
- medias
- media_files
- organizations
- people
- devices
- sampling_events
- locations
- occurences
- taxa
- identifications
- acoustic_events

Additionally, it imports the associations for captures_rel.
"""

# noqa
from . import (
    datasets,  # noqa
    medias,  # noqa
    media_files,  # noqa
    organizations,  # noqa
    people,  # noqa
    devices,  # noqa
    sampling_events,  # noqa
    locations,  # noqa
    occurences,  # noqa
    taxa,  # noqa
    identifications,  # noqa
    acoustic_events,  # noqa
)

from .associations import captures_rel  # noqa
