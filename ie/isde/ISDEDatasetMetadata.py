import urllib.request

import warnings
import json
import xmltodict

from owslib.iso import MD_Metadata, etree
from rdflib import Graph, URIRef, Literal, BNode

from .ComplexTypes import ComplexTypes
from .RDFNamespaces import RDFNamespaces
from .IANAMimeTypes import IANAMimeTypes
from .Licenses import Licenses


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
    base_uri: str = None
    """
    The base URI to use in building a graph data model representation of the Dataset object
    """
    bounding_box: dict = None
    """
    The geographic bounding box encompassing the data described byb the metadata object. The `dict` is defined by 
    `ComplexTypes.BOUNDING_BOX`.
    """
    date_issued: str = None
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
    license: dict = None
    """
    The license applied to the dataset.
    
    Note:
        When building from an ISO19139 XML document, the licence is extracted from `gmd:useLimitation` elements
    """
    temporal_extent: dict = None
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
    topic_categories: list = None
    """
    A list of strings giving the lexical labels of topic categories for this Dataset object
    """
    use_limitations: list = None
    """
    A list of strings describing any constraints for use on the dataset
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
                self.topic_categories = md.identification.topiccategory
            except AttributeError:
                pass
            # Extract the Date Issued
            try:
                self.date_issued = md.datestamp
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
                self.bounding_box = ComplexTypes.BOUNDING_BOX.value.copy()
                self.bounding_box['north'] = float(md.identification.bbox.maxy)
                self.bounding_box['south'] = float(md.identification.bbox.miny)
                self.bounding_box['west'] = float(md.identification.bbox.minx)
                self.bounding_box['east'] = float(md.identification.bbox.maxx)
            except AttributeError:
                pass
            # Extract start and end dates
            try:
                self.temporal_extent = ComplexTypes.TIMEPERIOD.value.copy()
                self.temporal_extent['start'] = md.identification.temporalextent_start
            except AttributeError:
                pass

            try:
                self.temporal_extent['end'] = md.identification.temporalextent_end
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
                for limit in md.identification.uselimitation:
                    if limit == "Creative Commons CC-BY 4.0":
                        self.license = Licenses.CCBY.value
                    else:
                        if self.use_limitations is None:
                            self.use_limitations = []
                        self.use_limitations.append(limit)
            except AttributeError:
                pass
            metadata.close()

        with urllib.request.urlopen(url) as metadata:
            md_dict = xmltodict.parse(metadata.read())
            if self.license is None:
                try:
                    resource_constraints = \
                        md_dict["gmd:MD_Metadata"]["gmd:identificationInfo"]["gmd:MD_DataIdentification"][
                            "gmd:resourceConstraints"]
                    for rc in resource_constraints:
                        try:
                            lics = rc["gmd:MD_Constraints"]["gmd:useLimitation"]
                            for lic in lics:
                                try:
                                    # print(lic["gmd:MD_ClassificationCode"]["#text"])
                                    if lic["gmd:MD_ClassificationCode"]["#text"] == "CC-By 4.0":
                                        self.license = Licenses.CCBY.value
                                except KeyError:
                                    pass
                        except KeyError:
                            pass
                except KeyError:
                    pass
            metadata.close()
        self.base_uri = url
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
        g.bind(RDFNamespaces.SKOS['ns'], RDFNamespaces.SKOS['url'])

        g.add((URIRef(self.base_uri), URIRef(RDFNamespaces.RDF['url'] + 'type'),
               URIRef(RDFNamespaces.DCAT['url'] + 'Dataset')))
        if self.title is not None:
            g.add((URIRef(self.base_uri), URIRef(RDFNamespaces.DCT['url'] + 'title'), Literal(self.title)))
        if self.abstract is not None:
            g.add((URIRef(self.base_uri), URIRef(RDFNamespaces.DCT['url'] + 'description'), Literal(self.abstract)))
        if self.identifier is not None:
            g.add((URIRef(self.base_uri), URIRef(RDFNamespaces.DCT['url'] + 'identifier'), Literal(self.identifier)))
        if self.date_issued is not None:
            g.add((URIRef(self.base_uri), URIRef(RDFNamespaces.DCT['url'] + 'issued'), Literal(self.date_issued)))
        if self.keywords is not None:
            for kws in self.keywords:
                for kw in kws.keyword:
                    g.add((URIRef(self.base_uri), URIRef(RDFNamespaces.DCAT['url'] + 'keyword'),
                           Literal(kw.name)))

        for topic in self.topic_categories:
            g.add((URIRef(self.base_uri), URIRef(RDFNamespaces.DCAT['url'] + 'theme'), Literal(topic)))

        if self.bounding_box is not None:
            spatial_node = BNode()

            g.add((URIRef(self.base_uri), URIRef(RDFNamespaces.DCT['url'] + 'spatial'), spatial_node))
            g.add((spatial_node, URIRef(RDFNamespaces.RDF['url'] + 'type'),
                   URIRef(RDFNamespaces.DCT['url'] + 'Location')))
            g.add((spatial_node, URIRef(RDFNamespaces.LOCN['url'] + 'geometry'),
                   Literal(self.bounding_box_to_wkt(), datatype=RDFNamespaces.GSP['url'] + 'wktLiteral')))
            g.add((spatial_node, URIRef(RDFNamespaces.LOCN['url'] + 'geometry'),
                   Literal(self.bounding_box_to_geojson(), datatype=IANAMimeTypes.GEOJSON.value)))

        if self.temporal_extent is not None:
            temporal_node = BNode()
            g.add((URIRef(self.base_uri), URIRef(RDFNamespaces.DCT['url'] + 'temporal'), temporal_node))
            g.add((temporal_node, URIRef(RDFNamespaces.RDF['url'] + 'type'),
                   URIRef(RDFNamespaces.DCT['url'] + 'PeriodOfTime')))
            if self.temporal_extent['start'] is not None:
                g.add((temporal_node, URIRef(RDFNamespaces.SDO['url'] + 'startDate'),
                       Literal(self.temporal_extent['start'])))
            if self.temporal_extent['end'] is not None:
                g.add((temporal_node, URIRef(RDFNamespaces.SDO['url'] + 'endDate'),
                       Literal(self.temporal_extent['end'])))

        for dist in self.distribution:
            if dist['protocol'] == 'WWW:DOWNLOAD-1.0-http--download':
                if dist['url'] is not None:
                    dist_node = BNode()
                    g.add((URIRef(self.base_uri), URIRef(RDFNamespaces.DCAT['url'] + 'distribution'), dist_node))
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
                    if self.license is not None:
                        g.add((dist_node, URIRef(RDFNamespaces.DCT['url'] + 'license'), URIRef(self.license['url'])))
                        g.add((URIRef(self.license['url']), URIRef(RDFNamespaces.RDF['url'] + 'type'),
                               URIRef(RDFNamespaces.DCT['url'] + 'LicenseDocument')))
                    if self.use_limitations is not None:
                        dcat_limitations = None
                        for limit in self.use_limitations:
                            if limit.find(" ") or not limit.startswith('http://') or limit.startswith('https://'):
                                limit = '\"{0}\"'.format(limit)
                            if dcat_limitations is None:
                                dcat_limitations = limit
                            else:
                                dcat_limitations = '{0} , {1}'.format(dcat_limitations, limit)
                        dcat_limitations = '{' + format(dcat_limitations) + '}'
                        rights_node = BNode()
                        g.add((dist_node, URIRef(RDFNamespaces.DCT['url'] + 'rights'), rights_node))
                        g.add((rights_node, URIRef(RDFNamespaces.RDF['url'] + 'type'),
                               URIRef(RDFNamespaces.DCT['url'] + 'rightsStatement')))
                        g.add((rights_node, URIRef(RDFNamespaces.SKOS['url'] + 'prefLabel'), Literal(dcat_limitations)))
            else:
                if dist['url'] is not None:
                    g.add((URIRef(self.base_uri), URIRef(RDFNamespaces.RDFS['url'] + 'seeAlso'), URIRef(dist['url'])))
        return g

    def to_schema_org(self) -> Graph:
        """
        Converts an ISDEDatasetMetadata object to a Schema.org graph model
        
        Returns:
            `rdflib.graph.Graph` of the `ISDEDatasetMetadata` object serialised as a Schema.org Dataset
        """
        g = Graph()

        g.add((URIRef(self.base_uri), URIRef(RDFNamespaces.RDF['url'] + 'type'),
               URIRef(RDFNamespaces.SDO['url'] + 'Dataset')))

        if self.title is not None:
            g.add((URIRef(self.base_uri), URIRef(RDFNamespaces.SDO['url'] + 'name'), Literal(self.title)))
        if self.abstract is not None:
            g.add((URIRef(self.base_uri), URIRef(RDFNamespaces.SDO['url'] + 'description'), Literal(self.abstract)))
        if self.identifier is not None:
            g.add((URIRef(self.base_uri), URIRef(RDFNamespaces.SDO['url'] + 'identifier'), Literal(self.identifier)))
        if self.date_issued is not None:
            g.add((URIRef(self.base_uri), URIRef(RDFNamespaces.SDO['url'] + 'datePublished'),
                   Literal(self.date_issued)))

        if self.bounding_box is not None:
            spatial_node = BNode()
            geo_node = BNode()
            if self.bounding_box['west'] == self.bounding_box['east'] \
                    and self.bounding_box['north'] == self.bounding_box['south']:
                g.add((URIRef(self.base_uri), URIRef(RDFNamespaces.SDO['url'] + 'spatialCoverage'), spatial_node))
                g.add((spatial_node, URIRef(RDFNamespaces.RDF['url'] + 'type'),
                       URIRef(RDFNamespaces.SDO['url'] + 'Place')))
                g.add((spatial_node, URIRef(RDFNamespaces.SDO['url'] + 'geo'), geo_node))
                g.add((spatial_node, URIRef(RDFNamespaces.SDO['url'] + 'latitude'), self.bounding_box['north']))
                g.add((spatial_node, URIRef(RDFNamespaces.SDO['url'] + 'longitude'), self.bounding_box['west']))
                g.add((spatial_node, URIRef(RDFNamespaces.SDO['url'] + 'geo'), geo_node))
                g.add((geo_node, URIRef(RDFNamespaces.RDF['url'] + 'type'),
                       URIRef(RDFNamespaces.SDO['url'] + 'GeoCoordinates')))
                g.add((geo_node, URIRef(RDFNamespaces.SDO['url'] + 'latitude'), self.bounding_box['north']))
                g.add((geo_node, URIRef(RDFNamespaces.SDO['url'] + 'longitude'), self.bounding_box['west']))
            else:
                g.add((URIRef(self.base_uri), URIRef(RDFNamespaces.SDO['url'] + 'spatialCoverage'), spatial_node))
                g.add((spatial_node, URIRef(RDFNamespaces.RDF['url'] + 'type'),
                       URIRef(RDFNamespaces.SDO['url'] + 'Place')))
                g.add((spatial_node, URIRef(RDFNamespaces.SDO['url'] + 'geo'), geo_node))
                g.add((geo_node, URIRef(RDFNamespaces.RDF['url'] + 'type'),
                       URIRef(RDFNamespaces.SDO['url'] + 'GeoShape')))
                g.add((geo_node, URIRef(RDFNamespaces.SDO['url'] + 'box'),
                       Literal('{0} {1} {2} {3}'.format(self.bounding_box['south'], self.bounding_box['south'],
                                                        self.bounding_box['north'], self.bounding_box['east']))))

        if self.keywords is not None:
            for kws in self.keywords:
                for kw in kws.keyword:
                    if kw.url is not None:
                        g.add((URIRef(self.base_uri), URIRef(RDFNamespaces.SDO['url'] + 'keywords'),
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
        for topic in self.topic_categories:
            g.add((URIRef(self.base_uri), URIRef(RDFNamespaces.SDO['url'] + 'keywords'), Literal(topic)))

        if self.temporal_extent is not None:
            if self.temporal_extent['start'] is not None:
                if self.temporal_extent['end'] is not None:
                    temporal_extent = Literal('{0}/{1}'.format(self.temporal_extent['start'],
                                                               self.temporal_extent['end']))
                else:
                    temporal_extent = Literal('{0}/..'.format(self.temporal_extent['start']))
                g.add((URIRef(self.base_uri), URIRef(RDFNamespaces.SDO['url'] + 'temporalCoverage'), temporal_extent))
        for dist in self.distribution:
            if dist['protocol'] == 'WWW:DOWNLOAD-1.0-http--download':
                if dist['url'] is not None:
                    dist_node = BNode()
                    g.add((URIRef(self.base_uri), URIRef(RDFNamespaces.SDO['url'] + 'distribution'), dist_node))
                    g.add((dist_node, URIRef(RDFNamespaces.RDF['url'] + 'type'),
                           URIRef(RDFNamespaces.SDO['url'] + 'DataDownload')))
                    g.add((dist_node, URIRef(RDFNamespaces.SDO['url'] + 'contentUrl'), Literal(dist['url'])))
        if self.license is not None:
            g.add((URIRef(self.base_uri), URIRef(RDFNamespaces.SDO['url'] + 'license'), self.license['url']))
            g.add((URIRef(self.base_uri), URIRef(RDFNamespaces.SDO['url'] + 'license'), self.license['spdx_url']))
        if self.use_limitations is not None:
            dcat_limitations = None
            for limit in self.use_limitations:
                if limit.find(" ") or not limit.startswith('http://') or limit.startswith('https://'):
                    limit = '\"{0}\"'.format(limit)
                if dcat_limitations is None:
                    dcat_limitations = limit
                else:
                    dcat_limitations = '{0} , {1}'.format(dcat_limitations, limit)
            dcat_limitations = '{' + format(dcat_limitations) + '}'
            g.add((URIRef(self.base_uri), URIRef(RDFNamespaces.SDO['url'] + 'usageInfo'), Literal(dcat_limitations)))
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
            if self.bounding_box['west'] == self.bounding_box['east'] \
                    and self.bounding_box['north'] == self.bounding_box['south']:
                return "POINT ({0} {1})".format(str(self.bounding_box['west']), str(self.bounding_box['south']))
            else:
                return "POLYGON (({0} {1},{2} {3},{4} {5},{6} {7},{8} {9}))".format(str(self.bounding_box['west']),
                                                                                    str(self.bounding_box['south']),
                                                                                    str(self.bounding_box['west']),
                                                                                    str(self.bounding_box['north']),
                                                                                    str(self.bounding_box['east']),
                                                                                    str(self.bounding_box['north']),
                                                                                    str(self.bounding_box['east']),
                                                                                    str(self.bounding_box['south']),
                                                                                    str(self.bounding_box['east']),
                                                                                    str(self.bounding_box['north']))
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
            if self.bounding_box['west'] == self.bounding_box['east'] \
                    and self.bounding_box['north'] == self.bounding_box['south']:
                return json.dumps({"type": "Point",
                                   "coordinates": [self.bounding_box['west'], self.bounding_box['south']]})
            else:
                return json.dumps({"type": "Polygon", "coordinates": [[
                    [self.bounding_box['west'], self.bounding_box['south']],
                    [self.bounding_box['west'], self.bounding_box['north']],
                    [self.bounding_box['east'], self.bounding_box['north']],
                    [self.bounding_box['east'], self.bounding_box['south']],
                    [self.bounding_box['west'], self.bounding_box['south']]]]})
        except TypeError:
            raise TypeError
