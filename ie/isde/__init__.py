"""
A package for working with metadata from the Irish Spatial Data Exchange
"""

from .Namespaces import ISDERDFNamespaces, ISDEXMLNamespaces
from .ISDEDatasetParser import ISDEDatasetParser
from .ISDEDatasetMetadata import ISDEDatasetMetadata

__all__ = ['ISDERDFNamespaces', 
           'ISDEDatasetParser', 
           'ISDEXMLNamespaces',
           'ISDEDatasetMetadata']