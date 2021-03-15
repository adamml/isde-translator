"""
Enumerates the Resource Description Framework and XML namespaces in use in ISDE
"""


class ISDERDFNamespaces:
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
    RDFS = {'ns': 'rdfs', 'url': 'http://www.w3.org/2000/01/rdf-schema#'}
    """
    W3C Resource Description Framework Schema vocabulary
    """
    SDO = {'ns': 'sdo', 'url': 'https://schema.org/'}
    """
    Schema.org vocab
    """