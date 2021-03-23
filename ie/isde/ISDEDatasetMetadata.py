import urllib.request
import warnings
import json

import warnings
import json

from owslib.iso import MD_Metadata, etree
from rdflib import Graph, URIRef, Literal, BNode

from .ComplexTypes import ComplexTypes
from .RDFNamespaces import RDFNamespaces
from .IANAMimeTypes import IANAMimeTypes


class ISDEDatasetMetadata:
    """
    This class is for storing attributes relating to a Dataset object from the Irish
    Spatial Data Exchange and provides methods to translate between serializations of
    the Dataset metadata
    
    Note:
        Two `FutureWarnings `warnings from the `owslib` are suppressed by the code for this class: 
        
        - One on merging the .identification attribute
        - One on merging the .keywords and .keywords2 attributes
    """
    warnings.filterwarnings("ignore", message="the .identification", category=FutureWarning, module="owslib")
    warnings.filterwarnings("ignore", message="the .keywords", category=FutureWarning, module="owslib")


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
    The geographic bounding box encompassing the data described byb the metadata object. The `dict` is defined by 
    `ComplexTypes.BOUNDING_BOX`.
    """
    dateIssued: str = None
    """
    The date on which the metadata record was issued
    """
    distribution: list = None
    """
    The various distribution methods for the dataset described by the metadata object. The attribute is a `list` of
    `dicts` where the `dict` is defined by `ComplexTypes.DISTRIBUTION`.
    
    Note:
        The `distribution` may be a download service, or a link to wither a view service or more information. Only
        download services are rendered as distributions in DCAT and Schema.org
    """
    identifier: str = None
    """
    A unique identifier to this Dataset object
    """
    keywords: list = None
    """
    A list of Keywords describing the metadata object, conforming to the `owslib.iso.MD_Keywords class`
    """
    license: list = None
    """
    The license applied to the dataset.
    
    Note:
        When building from an ISO19139 XML document, the licence is extracted from `gmd:useLimitation` elements
    """
    temporalExtent: dict = None
    """
    The time range of the dataset described by the metadata object as a `dict` with keys of `start` and `end`. The 
    `dict` is defined by `ComplexTypes.TIMEPERIOD`. 
    
    Note:
        For ongoing datasets, the value of `end` should be set to `None`
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
        Reads an Irish Spatial Data Exchange record from a given URL and populates the `ISDEDatasetMetadata` class
        attributes appropriately.
        
        Args:
            url: A `str` representing the URL from which to read the ISO 19139 XML file
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
            # Extract distributions
            try:
                print(md.distribution.online.name)
            except AttributeError:
                pass
            # Extract geographic bounding box
            try:
                self.boundingBox = ComplexTypes.BOUNDING_BOX.value.copy()
                self.boundingBox['north'] = float(md.identification.bbox.maxy)
                self.boundingBox['south'] = float(md.identification.bbox.miny)
                self.boundingBox['west'] = float(md.identification.bbox.minx)
                self.boundingBox['east'] = float(md.identification.bbox.maxx)
            except AttributeError:
                pass
            # Extract start and end dates
            try:
                self.temporalExtent = ComplexTypes.TIMEPERIOD.value.copy()
                self.temporalExtent['start'] = md.identification.temporalextent_start
            except AttributeError:
                pass
              
            try:
                self.temporalExtent['end'] = md.identification.temporalextent_end
            except AttributeError:
                pass

            try:
                self.distribution = []
                for ol in md.distribution.online:
                    dist = ComplexTypes.DISTRIBUTION.value.copy()
                    if ol.name is not None:
                        dist['name'] = ol.name
                    if ol.url is not None:
                        dist['url'] = ol.url
                    if ol.function is not None:
                        dist['function'] = ol.function
                    if ol.protocol is not None:
                        dist['protocol'] = ol.protocol
                    if ol.description is not None:
                        dist['description'] = ol.description
                    self.distribution.append(dist)
            except AttributeError:
                pass

            try:
                print(md.identification.uselimitation)
            except AttributeError:
                pass

        self.baseURI = url
        return self

    def to_dcat(self) -> Graph:
        """
        Converts an `ISDEDatasetMetadata` object to a W3C Data Catalog Vocabulary model
        
        Returns:
            `rdflib.graph.Graph` of the `ISDEDatasetMetadata` object serialised as a W3C Data Catalog
            Vocabulary (DCAT) Dataset
        """
        g = Graph()
        g.bind(RDFNamespaces.DCAT['ns'], RDFNamespaces.DCAT['url'])
        g.bind(RDFNamespaces.DCT['ns'], RDFNamespaces.DCT['url'])
        g.bind(RDFNamespaces.GSP['ns'], RDFNamespaces.GSP['url'])
        g.bind(RDFNamespaces.LOCN['ns'], RDFNamespaces.LOCN['url'])
        g.bind(RDFNamespaces.RDF['ns'], RDFNamespaces.RDF['url'])
        g.bind(RDFNamespaces.RDFS['ns'], RDFNamespaces.RDFS['url'])
        g.bind(RDFNamespaces.SDO['ns'], RDFNamespaces.SDO['url'])

        g.add((URIRef(self.baseURI), URIRef(RDFNamespaces.RDF['url'] + 'type'),
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
            g.add((spatial_node, URIRef(RDFNamespaces.RDF['url'] + 'type'),
                   URIRef(RDFNamespaces.DCT['url'] + 'Location')))
            g.add((spatial_node, URIRef(RDFNamespaces.LOCN['url'] + 'geometry'),
                   Literal(self.bounding_box_to_wkt(), datatype=RDFNamespaces.GSP['url'] + 'wktLiteral')))
            g.add((spatial_node, URIRef(RDFNamespaces.LOCN['url'] + 'geometry'),
                   Literal(self.bounding_box_to_geojson(), datatype=IANAMimeTypes.GEOJSON.value)))

        if self.temporalExtent is not None:
            temporal_node = BNode()
            g.add((URIRef(self.baseURI), URIRef(RDFNamespaces.DCT['url'] + 'temporal'), temporal_node))
            g.add((temporal_node, URIRef(RDFNamespaces.RDF['url'] + 'type'),
                   URIRef(RDFNamespaces.DCT['url'] + 'PeriodOfTime')))
            if self.temporalExtent['start'] is not None:
                g.add((temporal_node, URIRef(RDFNamespaces.SDO['url'] + 'startDate'),
                       Literal(self.temporalExtent['start'])))
            if self.temporalExtent['end'] is not None:
                g.add((temporal_node, URIRef(RDFNamespaces.SDO['url'] + 'endDate'),
                       Literal(self.temporalExtent['end'])))

        for dist in self.distribution:
            if dist['protocol'] == 'WWW:DOWNLOAD-1.0-http--download':
                if dist['url'] is not None:
                    dist_node = BNode()
                    g.add((URIRef(self.baseURI), URIRef(RDFNamespaces.DCAT['url'] + 'distribution'), dist_node))
                    g.add((dist_node, URIRef(RDFNamespaces.RDF['url'] + 'type'),
                           URIRef(RDFNamespaces.DCAT['url'] + 'Distribution')))
                    g.add((dist_node, URIRef(RDFNamespaces.DCAT['url'] + 'accessURL'), URIRef(dist['url'])))
                    if dist['name'] is not None:
                        g.add((dist_node, URIRef(RDFNamespaces.DCT['url'] + 'title'), Literal(dist['name'])))
                    elif dist['description'] is not None:
                        g.add((dist_node, URIRef(RDFNamespaces.DCT['url'] + 'title'), Literal(dist['description'])))
                    if dist['description'] is not None:
                        g.add(
                            (dist_node, URIRef(RDFNamespaces.DCT['url'] + 'description'), Literal(dist['description'])))
                    elif dist['name'] is not None:
                        g.add((dist_node, URIRef(RDFNamespaces.DCT['url'] + 'description'), Literal(dist['name'])))
            else:
                if dist['url'] is not None:
                    g.add((URIRef(self.baseURI), URIRef(RDFNamespaces.RDFS['url'] + 'seeAlso'), URIRef(dist['url'])))


        return g

    def to_schema_org(self) -> Graph:
        """
        Converts an ISDEDatasetMetadata object to a Schema.org graph model
        
        Returns:
            `rdflib.graph.Graph` of the `ISDEDatasetMetadata` object serialised as a Schema.org Dataset
        """
        g = Graph()

        g.add((URIRef(self.baseURI), URIRef(RDFNamespaces.RDF['url'] + 'type'),
               URIRef(RDFNamespaces.SDO['url'] + 'Dataset')))

        if self.title is not None:
            g.add((URIRef(self.baseURI), URIRef(RDFNamespaces.SDO['url'] + 'name'), Literal(self.title)))
        if self.abstract is not None:
            g.add((URIRef(self.baseURI), URIRef(RDFNamespaces.SDO['url'] + 'description'), Literal(self.abstract)))
        if self.identifier is not None:
            g.add((URIRef(self.baseURI), URIRef(RDFNamespaces.SDO['url'] + 'identifier'), Literal(self.identifier)))
        if self.dateIssued is not None:
            g.add((URIRef(self.baseURI), URIRef(RDFNamespaces.SDO['url'] + 'datePublished'),
                   Literal(self.dateIssued)))

        if self.boundingBox is not None:
            spatial_node = BNode()
            geo_node = BNode()
            if self.boundingBox['west'] == self.boundingBox['east'] \
                    and self.boundingBox['north'] == self.boundingBox['south']:
                g.add((URIRef(self.baseURI), URIRef(RDFNamespaces.SDO['url'] + 'spatialCoverage'), spatial_node))
                g.add((spatial_node, URIRef(RDFNamespaces.RDF['url'] + 'type'),
                       URIRef(RDFNamespaces.SDO['url'] + 'Place')))
                g.add((spatial_node, URIRef(RDFNamespaces.SDO['url'] + 'geo'), geo_node))
                g.add((spatial_node, URIRef(RDFNamespaces.SDO['url'] + 'latitude'), self.boundingBox['north']))
                g.add((spatial_node, URIRef(RDFNamespaces.SDO['url'] + 'longitude'), self.boundingBox['west']))
                g.add((spatial_node, URIRef(RDFNamespaces.SDO['url'] + 'geo'), geo_node))
                g.add((geo_node, URIRef(RDFNamespaces.RDF['url'] + 'type'),
                       URIRef(RDFNamespaces.SDO['url'] + 'GeoCoordinates')))
                g.add((geo_node, URIRef(RDFNamespaces.SDO['url'] + 'latitude'), self.boundingBox['north']))
                g.add((geo_node, URIRef(RDFNamespaces.SDO['url'] + 'longitude'), self.boundingBox['west']))
            else:
                g.add((URIRef(self.baseURI), URIRef(RDFNamespaces.SDO['url'] + 'spatialCoverage'), spatial_node))
                g.add((spatial_node, URIRef(RDFNamespaces.RDF['url'] + 'type'),
                       URIRef(RDFNamespaces.SDO['url'] + 'Place')))
                g.add((spatial_node, URIRef(RDFNamespaces.SDO['url'] + 'geo'), geo_node))
                g.add((geo_node, URIRef(RDFNamespaces.RDF['url'] + 'type'),
                       URIRef(RDFNamespaces.SDO['url'] + 'GeoShape')))
                g.add((geo_node, URIRef(RDFNamespaces.SDO['url'] + 'box'),
                       Literal('{0} {1} {2} {3}'.format(self.boundingBox['south'], self.boundingBox['south'],
                                                        self.boundingBox['north'], self.boundingBox['east']))))

        if self.keywords is not None:
            for kws in self.keywords:
                for kw in kws.keyword:
                    if kw.url is not None:
                        g.add((URIRef(self.baseURI), URIRef(RDFNamespaces.SDO['url'] + 'keywords'),
                               URIRef(kw.url)))

                        g.add((URIRef(kw.url), URIRef(RDFNamespaces.RDF['url'] + 'type'),

                               URIRef(RDFNamespaces.SDO['url'] + 'DefinedTerm')))
                    if kw.name is not None:
                        g.add((URIRef(kw.url), URIRef(RDFNamespaces.SDO['url'] + 'name'),
                               Literal(kw.name)))
                    if kws.thesaurus['url'] is not None:
                        g.add((URIRef(kw.url), URIRef(RDFNamespaces.SDO['url'] + 'inDefinedTermSet'),
                               Literal(kws.thesaurus['url'])))

                        g.add((URIRef(kws.thesaurus['url']), URIRef(RDFNamespaces.RDF['url'] + 'type'),

                               URIRef(RDFNamespaces.SDO['url'] + 'DefinedTermSet')))
                    if kws.thesaurus['title'] is not None:
                        g.add((URIRef(kws.thesaurus['url']), URIRef(RDFNamespaces.SDO['url'] + 'name'),
                               Literal(kws.thesaurus['title'])))
        for topic in self.topicCategories:
            g.add((URIRef(self.baseURI), URIRef(RDFNamespaces.SDO['url'] + 'keywords'), Literal(topic)))

        if self.temporalExtent is not None:
            if self.temporalExtent['start'] is not None:
                if self.temporalExtent['end'] is not None:
                    temporal_extent = Literal('{0}/{1}'.format(self.temporalExtent['start'],
                                                               self.temporalExtent['end']))
                else:
                    temporal_extent = Literal('{0}/..'.format(self.temporalExtent['start']))
                g.add((URIRef(self.baseURI), URIRef(RDFNamespaces.SDO['url'] + 'temporalCoverage'), temporal_extent))
        for dist in self.distribution:
            if dist['protocol'] == 'WWW:DOWNLOAD-1.0-http--download':
                if dist['url'] is not None:
                    dist_node = BNode()
                    g.add((URIRef(self.baseURI), URIRef(RDFNamespaces.SDO['url'] + 'distribution'), dist_node))
                    g.add((dist_node, URIRef(RDFNamespaces.RDF['url'] + 'type'),
                          URIRef(RDFNamespaces.SDO['url'] + 'DataDownload')))
                    g.add((dist_node, URIRef(RDFNamespaces.SDO['url'] + 'contentUrl'), Literal(dist['url'])))
        return g

    def bounding_box_to_wkt(self) -> str:
        """
        Converts the geographic bounding box of the metadata object to a Well Known Text string

        Returns:
            `str` containing the geographic bounding box encoded as Well Known Text

        Raises:
            `TypeError` if the `ISDEDatasetMetadata` object's boundingBox attribute is not set
        """
        try:
            if self.boundingBox['west'] == self.boundingBox['east'] \
                    and self.boundingBox['north'] == self.boundingBox['south']:
                return "POINT ({0} {1})".format(str(self.boundingBox['west']), str(self.boundingBox['south']))
            else:
                return "POLYGON (({0} {1},{2} {3},{4} {5},{6} {7},{8} {9}))".format(str(self.boundingBox['west']),
                                                                                    str(self.boundingBox['south']),
                                                                                    str(self.boundingBox['west']),
                                                                                    str(self.boundingBox['north']),
                                                                                    str(self.boundingBox['east']),
                                                                                    str(self.boundingBox['north']),
                                                                                    str(self.boundingBox['east']),
                                                                                    str(self.boundingBox['south']),
                                                                                    str(self.boundingBox['east']),
                                                                                    str(self.boundingBox['north']))
        except TypeError:
            raise TypeError

    def bounding_box_to_geojson(self) -> str:
        """
        Converts the geographic bounding box of the metadata object to a GeoJSON string

        Returns:
            `str` containing the geographic bounding box encoded as GeoJSON

        Raises:
            `TypeError` if the `ISDEDatasetMetadata` object's boundingBox attribute is not set
        """
        try:
            if self.boundingBox['west'] == self.boundingBox['east'] \
                    and self.boundingBox['north'] == self.boundingBox['south']:
                return json.dumps({"type": "Point",
                                   "coordinates": [self.boundingBox['west'], self.boundingBox['south']]})
            else:
                return json.dumps({"type": "Polygon", "coordinates": [[
                                   [self.boundingBox['west'], self.boundingBox['south']],
                                   [self.boundingBox['west'], self.boundingBox['north']],
                                   [self.boundingBox['east'], self.boundingBox['north']],
                                   [self.boundingBox['east'], self.boundingBox['south']],
                                   [self.boundingBox['west'], self.boundingBox['south']]]]})
        except TypeError:
            raise TypeError
