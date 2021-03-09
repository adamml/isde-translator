"""
Enumerates the XPath queries to extract information from ISO 19139 files
"""
class ISDEDatasetParser:
    """
    This class extends the IsoParser from `gis_metadata.iso_metadata_parser` to handle
    Irish Spatial Data Exchange Dataset Metadata.
    """
    TITLE = "./gmd:identificationInfo/gmd:MD_DataIdentification/gmd:citation/gmd:CI_Citation/gmd:title/gco:CharacterString"
    """
    XPath to get the lexical title of a dataset
    """
    ABSTRACT = "./gmd:identificationInfo/gmd:MD_DataIdentification/gmd:abstract/gco:CharacterString"
    """
    XPath to get the abstract of a dataset
    """
    IDENTIFIER = "./gmd:fileIdentifier/gco:CharacterString"
    """
    XPath to get the file identifier of a dataset
    """
    DATEISSUED = "./gmd:dateStamp/gco:Date"
    """
    XPAth to get the date a metadata object was issued
    """