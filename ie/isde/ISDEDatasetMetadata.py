import urllib.request

from owslib.iso import MD_Metadata, etree

from .ComplexTypes import ComplexTypes

from .RDFNamespaces import RDFNamespaces

from .IANAMimeTypes import IANAMimeTypes

from rdflib import Graph, URIRef, Literal, BNode

import warnings

import json

warnings.filterwarnings("ignore", message="the .identification", category=FutureWarning, module="owslib")
warnings.filterwarnings("ignore", message="the .keywords", category=FutureWarning, module="owslib")


class ISDEDatasetMetadata:
    """
    This class is for storing attributes relating to a Dataset object from the Irish
    Spatial Data Exchange and provides methods to translate between serializations of
    the Dataset metadata
    """
    _metadata = None

    abstract: str = None
    """
    The abstract giving a detailed description of the Dataset object
    """
    baseURI: str = None
    """
    The base URI to use in building a graph data model representation of the Dataset object
    """
    boundingBox: dict = None
    """
    The geographic bounding box encompassing the data described byb the metadata object
    """
    dateIssued: str = None
    """
    The date on which the metadata record was issued
    """
    identifier: str = None
    """
    A unique identifier to this Dataset object
    """
    keywords: list = None
    """
    A list of Keywords describing the metadata object, conforming to the `owslib.iso.MD_Keywords class`
    """
    title: str = None
    """
    The lexical title of the Dataset object
    """
    topicCategories: list = None
    """
    A list of strings giving the lexical labels of topic categories for this Dataset object
    """

    def __init__(self):
        pass

    def from_iso(self, url: str):
        """
        The from_iso method reads an Irish Spatial Data Exchange record from a given URL and
        populates the ISDEDatasetMetadata class attributes appropriately.
        
        :arg: url: A string representing the URL from which to read the ISO 19139 XML file
        """
        with urllib.request.urlopen(url) as metadata:
            md = MD_Metadata(etree.parse(metadata))
            # Extract Title
            try:
                self.title = md.identification.title
            except AttributeError:
                pass
            # Extract Abstract
            try:
                self.abstract = md.identification.abstract
            except AttributeError:
                pass
            # Extract Identifier
            try:
                self.identifier = md.identifier
            except AttributeError:
                pass
            # Extract Topic Categories
            try:
                self.topicCategories = md.identification.topiccategory
            except AttributeError:
                pass
            # Extract the Date Issued
            try:
                self.dateIssued = md.datestamp
            except AttributeError:
                pass
            # Extract keywords
            try:
                self.keywords = []
                for kw in md.identification.keywords2:
                    self.keywords.append(kw)
            except AttributeError:
                pass
            # Extract distibutions
            try:
                print(md.distribution.online.name)
            except AttributeError:
                pass
            # Extract geograhic bounding box
            try:
                self.boundingBox = ComplexTypes.BOUNDING_BOX.value
                self.boundingBox['north'] = md.identification.bbox.maxy
                self.boundingBox['south'] = md.identification.bbox.miny
                self.boundingBox['west'] = md.identification.bbox.minx
                self.boundingBox['east'] = md.identification.bbox.maxx
            except AttributeError:
                pass

        self.baseURI = url
        return self

    def to_dcat(self):
        """
        Converts an ISDEDatasetMetadata object to a W3C Data Catlog Vocabulary model
        
        :return: A `rdflib.Graph` of the ISDEDatasetMetadata object serialised as a W3C Data Catalog
            Vocabulary (DCAT) Dataset
        """
        g = Graph()
        g.bind(RDFNamespaces.DCAT['ns'], RDFNamespaces.DCAT['url'])
        g.bind(RDFNamespaces.DCT['ns'], RDFNamespaces.DCT['url'])
        g.bind(RDFNamespaces.GSP['ns'], RDFNamespaces.GSP['url'])
        g.bind(RDFNamespaces.LOCN['ns'], RDFNamespaces.LOCN['url'])
        g.bind(RDFNamespaces.RDFS['ns'], RDFNamespaces.RDFS['url'])

        g.add((URIRef(self.baseURI), URIRef(RDFNamespaces.RDFS['url'] + 'type'),
               URIRef(RDFNamespaces.DCAT['url'] + 'Dataset')))
        if self.title is not None:
            g.add((URIRef(self.baseURI), URIRef(RDFNamespaces.DCT['url'] + 'title'), Literal(self.title)))
        if self.abstract is not None:
            g.add((URIRef(self.baseURI), URIRef(RDFNamespaces.DCT['url'] + 'description'), Literal(self.abstract)))
        if self.identifier is not None:
            g.add((URIRef(self.baseURI), URIRef(RDFNamespaces.DCT['url'] + 'identifier'), Literal(self.identifier)))
        if self.dateIssued is not None:
            g.add((URIRef(self.baseURI), URIRef(RDFNamespaces.DCT['url'] + 'issued'), Literal(self.dateIssued)))
        if self.keywords is not None:
            for kws in self.keywords:
                for kw in kws.keyword:
                    g.add((URIRef(self.baseURI), URIRef(RDFNamespaces.DCAT['url'] + 'keyword'),
                           Literal(kw.name)))

        for topic in self.topicCategories:
            g.add((URIRef(self.baseURI), URIRef(RDFNamespaces.DCAT['url'] + 'theme'), Literal(topic)))

        if self.boundingBox is not None:
            spatial_node = BNode()

            g.add((URIRef(self.baseURI), URIRef(RDFNamespaces.DCT['url'] + 'spatial'), spatial_node))
            g.add((spatial_node, URIRef(RDFNamespaces.RDFS['url'] + 'type'),
                   URIRef(RDFNamespaces.DCT['url'] + 'location')))
            g.add((spatial_node, URIRef(RDFNamespaces.RDFS['url'] + 'type'),
                   URIRef(RDFNamespaces.LOCN['url'] + 'geometry')))
            g.add((spatial_node, URIRef(RDFNamespaces.LOCN['url'] + 'geometry'),
                   Literal(self.bounding_box_to_wkt(), datatype=RDFNamespaces.GSP['url'] + 'wktLiteral')))
            g.add((spatial_node, URIRef(RDFNamespaces.LOCN['url'] + 'geometry'),
                   Literal(self.bounding_box_to_geojson(), datatype=IANAMimeTypes.GEOJSON.value)))

        return g

    def to_schema_org(self):
        """
        Converts an ISDEDatasetMetadata object to a Schema.org graph model
        
        :return: `rdflib.Graph` of the ISDEDatasetMetadata object serialised as a Schema.org Dataset
        """
        g = Graph()

        if self.title is not None:
            g.add((URIRef(self.baseURI), URIRef(RDFNamespaces.SDO['url'] + 'name'), Literal(self.title)))
        if self.abstract is not None:
            g.add((URIRef(self.baseURI), URIRef(RDFNamespaces.SDO['url'] + 'description'), Literal(self.abstract)))
        if self.identifier is not None:
            g.add((URIRef(self.baseURI), URIRef(RDFNamespaces.SDO['url'] + 'identifier'), Literal(self.identifier)))
        if self.dateIssued is not None:
            g.add((URIRef(self.baseURI), URIRef(RDFNamespaces.SDO['url'] + 'datePublished'),
                   Literal(self.dateIssued)))
        if self.keywords is not None:
            for kws in self.keywords:
                for kw in kws.keyword:
                    if kw.url is not None:
                        g.add((URIRef(self.baseURI), URIRef(RDFNamespaces.SDO['url'] + 'keywords'),
                               URIRef(kw.url)))
                        g.add((URIRef(kw.url), URIRef(RDFNamespaces.RDFS['url'] + 'type'),
                               URIRef(RDFNamespaces.SDO['url'] + 'DefinedTerm')))
                    if kw.name is not None:
                        g.add((URIRef(kw.url), URIRef(RDFNamespaces.SDO['url'] + 'name'),
                               Literal(kw.name)))
                    if kws.thesaurus['url'] is not None:
                        g.add((URIRef(kw.url), URIRef(RDFNamespaces.SDO['url'] + 'inDefinedTermSet'),
                               Literal(kws.thesaurus['url'])))
                        g.add((URIRef(kws.thesaurus['url']), URIRef(RDFNamespaces.RDFS['url'] + 'type'),
                               URIRef(RDFNamespaces.SDO['url'] + 'DefinedTermSet')))
                    if kws.thesaurus['title'] is not None:
                        g.add((URIRef(kws.thesaurus['url']), URIRef(RDFNamespaces.SDO['url'] + 'name'),
                               Literal(kws.thesaurus['title'])))
        for topic in self.topicCategories:
            g.add((URIRef(self.baseURI), URIRef(RDFNamespaces.SDO['url'] + 'keywords'), Literal(topic)))
        return g

    def bounding_box_to_wkt(self):
        """
        Converts the geographic bounding box of the metadata object to a Well Known Text string

        :return: A string containing the geographic bounding box encoded as Well Known Text

        :raise: TypeError if the ISDEDatasetMetadata object's boundingBox attribute is not set
        """
        try:
            return "POLYGON ((" + self.boundingBox['west'] + " " + self.boundingBox['south'] + \
               "," + self.boundingBox['west'] + " " + self.boundingBox['north'] + "," + \
               self.boundingBox['east'] + " " + self.boundingBox['north'] + "," + \
               self.boundingBox['east'] + " " + self.boundingBox['south'] + "," + \
               self.boundingBox['east'] + " " + self.boundingBox['north'] + "))"
        except TypeError:
            raise TypeError

    def bounding_box_to_geojson(self):
        """
        Converts the geographic bounding box of the metadata object to a GeoJSON string

        :return: String containing the geographic bounding box encoded as GeoJSON

        :raise: TypeError if the ISDEDatasetMetadata object's boundingBox attribute is not set
        """
        try:
            return json.dumps({"type": "Polygon",
                  "coordinates": [[
                      [self.boundingBox['west'], self.boundingBox['south']],
                      [self.boundingBox['west'], self.boundingBox['north']],
                      [self.boundingBox['east'], self.boundingBox['north']],
                      [self.boundingBox['east'], self.boundingBox['south']],
                      [self.boundingBox['west'], self.boundingBox['south']]
                  ]]})
        except TypeError:
            raise TypeError
