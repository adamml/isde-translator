"""
This file enumerates IANA MIME Types in use in the Irish Spatial Data Exchange
"""

from enum import Enum


class IANAMimeTypes(Enum):
    """
    This class enumerates the IANA MIME Types in use in the Irish Spatial Data Exchange
    """
    CSV = "https://www.iana.org/assignments/media-types/text/csv",
    """
    `str` of the URL defining the IANA MIME Type for a Comma Separated Value file
    """
    GEOJSON = "https://www.iana.org/assignments/media-types/application/vnd.geo+json"
    """
    `str` of the URL defining the IANA MIME Type for JavaScript Object Notation encoded to the GeoJSON standard for 
    exchange of geographic data
    """