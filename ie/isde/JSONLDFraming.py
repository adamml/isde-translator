"""
This file enumerates JSON-LD Framing options to be used in serialising Irish Spatial Data Exchange metadata objects
"""

from enum import Enum

class JSONLDFraming(Enum):
    DATASET_SCHEMA_ORG = {"@context":
        {
            "@vocab": "https://schema.org/"
        },
        "@id": None
    }
    """
    Framing for a Schema.org Dataset
    """