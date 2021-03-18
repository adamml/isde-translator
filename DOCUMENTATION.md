Module isde
===========
A package for working with metadata from the Irish Spatial Data Exchange

Sub-modules
-----------
* isde.IANAMimeTypes

Classes
-------

`ComplexTypes(value, names=None, *, module=None, qualname=None, type=None, start=1)`
:   ComplexTypes enumerates the more complicated attribute types in use in Irish Spatial Data Exchange metadata objects

    ### Ancestors (in MRO)

    * enum.Enum

    ### Class variables

    `BOUNDING_BOX`
    :   The geographical bounding box of the metadata object

`ISDEDatasetMetadata()`
:   This class is for storing attributes relating to a Dataset object from the Irish
    Spatial Data Exchange and provides methods to translate between serializations of
    the Dataset metadata

    ### Class variables

    `abstract: str`
    :   The abstract giving a detailed description of the Dataset object

    `baseURI: str`
    :   The base URI to use in building a graph data model representation of the Dataset object

    `boundingBox: dict`
    :   The geographic bounding box encompassing the data described byb the metadata object

    `dateIssued: str`
    :   The date on which the metadata record was issued

    `identifier: str`
    :   A unique identifier to this Dataset object

    `keywords: list`
    :   A list of Keywords describing the metadata object, conforming to the `owslib.iso.MD_Keywords class`

    `title: str`
    :   The lexical title of the Dataset object

    `topicCategories: list`
    :   A list of strings giving the lexical labels of topic categories for this Dataset object

    ### Methods

    `bounding_box_to_geojson(self)`
    :   Converts the geographic bounding box of the metadata object to a GeoJSON string
        
        :return: String containing the geographic bounding box encoded as GeoJSON
        
        :raise: TypeError if the ISDEDatasetMetadata object's boundingBox attribute is not set

    `bounding_box_to_wkt(self)`
    :   Converts the geographic bounding box of the metadata object to a Well Known Text string
        
        :return: A string containing the geographic bounding box encoded as Well Known Text
        
        :raise: TypeError if the ISDEDatasetMetadata object's boundingBox attribute is not set

    `from_iso(self, url: str)`
    :   The from_iso method reads an Irish Spatial Data Exchange record from a given URL and
        populates the ISDEDatasetMetadata class attributes appropriately.
        
        :arg: url: A string representing the URL from which to read the ISO 19139 XML file

    `to_dcat(self)`
    :   Converts an ISDEDatasetMetadata object to a W3C Data Catlog Vocabulary model
        
        :return: A `rdflib.Graph` of the ISDEDatasetMetadata object serialised as a W3C Data Catalog
            Vocabulary (DCAT) Dataset

    `to_schema_org(self)`
    :   Converts an ISDEDatasetMetadata object to a Schema.org graph model
        
        :return: `rdflib.Graph` of the ISDEDatasetMetadata object serialised as a Schema.org Dataset

`RDFNamespaces()`
:   Resource Description Framework namespaces in use in the Irish Spatial Data
    Exchange

    ### Class variables

    `DCAT`
    :   W3C Data Catalog vocabulary

    `DCT`
    :   Dublin Core Terms

    `GSP`
    :   Open Geospatial Consortium GeoSPARQL ontology

    `LOCN`
    :   W3C Interoperable Solutions for Administrations (ISA) Programme Location Core Vocabulary

    `RDFS`
    :   W3C Resource Description Framework Schema vocabulary

    `SDO`
    :   Schema.org vocab
