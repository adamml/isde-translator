"""
This file contains definitions of complex type in use as attributes for Irish Spatial Data Exchange metadata objects
"""
from enum import Enum


class ComplexTypes(Enum):
    """
    ComplexTypes enumerates the more complicated attribute types in use in Irish Spatial Data Exchange metadata objects
    """
    BOUNDING_BOX = {"east": None, "north": None, "south": None, "west": None}
    """
    The geographical bounding box of the metadata object
    """
    DISTRIBUTION = {"description": None, "function": None, "name": None, "protocol": None, "url": None}
    """
    Links to download services, view services or more information about the digital object described by the metadata
    """
    KEYWORD = {"preferred_label": None, "url": None}
    """
    A Keyword used to describe the metadata object. A Keyword may come from a controlled vocabulary and be published 
    online with a URL.
    """
    LICENCE = {"name": None, "url": None}
    """
    The licence applied to the dataset
    """
    TIMEPERIOD = {"start": None, "end": None}
    """
    The temporal extent of the object described by the metadata
    """
