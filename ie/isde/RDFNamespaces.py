"""
Enumerates the Resource Description Framework and XML namespaces in use in ISDE
"""


class RDFNamespaces:
    """
    Resource Description Framework namespaces in use in the Irish Spatial Data
    Exchange
    """
    DCAT = {'ns': 'dcat', 'url': 'http://www.w3.org/ns/dcat#'}
    """
    W3C Data Catalog vocabulary
    """
    DCT = {'ns': 'dct', 'url': 'http://purl.org/dc/terms/'}
    """
    Dublin Core Terms
    """
    GSP = {'ns': 'gsp', 'url': 'http://www.opengis.net/ont/geosparql#'}
    """
    Open Geospatial Consortium GeoSPARQL ontology
    """
    LOCN = {'ns': 'locn', 'url': 'http://www.w3.org/ns/locn#'}
    """
    W3C Interoperable Solutions for Administrations (ISA) Programme Location Core Vocabulary
    """
    RDFS = {'ns': 'rdfs', 'url': 'http://www.w3.org/2000/01/rdf-schema#'}
    """
    W3C Resource Description Framework Schema vocabulary
    """
    SDO = {'ns': 'sdo', 'url': 'https://schema.org/'}
    """
    Schema.org vocab
    """