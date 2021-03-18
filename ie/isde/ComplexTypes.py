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
