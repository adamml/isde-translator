"""
Enumerates the Resource Description Framework and XML namespaces in use in ISDE.

Each class variable is a `dict` with two keys:
- _ns_: The preferred namespace prefix for the vocabulary as a `str`
- _url_: The URL to the vocabulary as a `str`
"""


class RDFNamespaces:
    """
    Resource Description Framework namespaces in use in the Irish Spatial Data
    Exchange

    Each class variable is a `dict` with two keys:
    - _ns_: The preferred namespace prefix for the vocabulary as a `str`
    - _url_: The URL to the vocabulary as a `str`
    """
    DCAT: dict = {'ns': 'dcat', 'url': 'http://www.w3.org/ns/dcat#'}
    """
    W3C Data Catalog vocabulary
    """
    DCT: dict = {'ns': 'dct', 'url': 'http://purl.org/dc/terms/'}
    """
    Dublin Core Terms
    """
    GSP: dict = {'ns': 'gsp', 'url': 'http://www.opengis.net/ont/geosparql#'}
    """
    Open Geospatial Consortium GeoSPARQL ontology
    """
    LOCN: dict = {'ns': 'locn', 'url': 'http://www.w3.org/ns/locn#'}
    """
    W3C Interoperable Solutions for Administrations (ISA) Programme Location Core Vocabulary
    """
    RDF: dict = {'ns': 'rdf', 'url': 'http://www.w3.org/1999/02/22-rdf-syntax-ns#'}
    """
    W3C Resource Description Framework concepts vocabulary
    """
    RDFS: dict = {'ns': 'rdfs', 'url': 'http://www.w3.org/2000/01/rdf-schema#'}
    """
    W3C Resource Description Framework Schema vocabulary
    """
    SDO: dict = {'ns': 'sdo', 'url': 'https://schema.org/'}
    """
    Schema.org vocab
    """