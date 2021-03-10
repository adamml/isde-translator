Module isde
===========
A package for working with metadata from the Irish Spatial Data Exchange

Classes
-------

`ISDEDatasetMetadata()`
:   This class is for storing attributes relating to a Dataset object from the Irish
    Spatial Data Exchange and provides methods to translate between serializations of
    the Dataset metadata

    ### Class variables

    `abstract: str`
    :   The abstract giving a detailed description of the Dataset object

    `baseURI: str`
    :   The vase URI to use in building a graph data model representation of the Dataset object

    `dateIssued: str`
    :   The date on which the metadata record was issued

    `identifier: str`
    :   A unique identifier to this Dataset object

    `title: str`
    :   The lexical title of the Dataset object

    `topicCategories: list`
    :   A list of strings giving the lexical labels of topic categories for this Dataset object

    ### Methods

    `fromISO(self, url: str)`
    :   The fromISO method reads an Irish Spatial Data Exchange record from a given URL and
        populates the ISDEDatasetMetadata class attributes appropiately.
        
        Args:
            url: A string representing the URL from which to read the ISO 19139 XML file

    `toDCAT(self)`
    :   Converts an ISDEDatasetMetadata object to a W3C Data Catlog Vocabulary model
        
        Returns:
            A `rdflib.Graph` of the ISDEDatasetMetadata object serialised as a W3C
            Data Catalog Vocabulary (DCAT) Dataset

    `toSchemaOrg(self)`
    :   Converts an ISDEDatasetMetadata object to a Schma.org graph model
        
        Returns:
            A `rdflib.Graph` of the ISDEDatasetMetadata object serialised as a
            Schema.org Dataset

`ISDERDFNamespaces()`
:   Resource Description Framework namespaces in use in the Irish Spatial Data
    Exchange

    ### Class variables

    `DCAT`
    :   W3C Data Catalog vocabulary

    `DCT`
    :   Dublin Core Terms

    `RDFS`
    :   W3C Resource Description Framework Schema vocabulary

    `SDO`
    :   Schema.org vocab

`ISDEXMLNamespaces()`
:   Enumerates the XML namespaces in use in the Irish Spatial data exchange

    ### Class variables

    `NAMESPACES`
    :

