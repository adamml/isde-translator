import urllib.request

from owslib.iso import MD_Metadata, etree

from ie.isde.ISDERDFNamespaces import ISDERDFNamespaces

from rdflib import Graph, URIRef, Literal

import warnings

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
    The vase URI to use in building a graph data model representation of the Dataset object
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

    def fromISO(self, url: str):
        """
        The fromISO method reads an Irish Spatial Data Exchange record from a given URL and
        populates the ISDEDatasetMetadata class attributes appropriately.
        
        Args:
            url: A string representing the URL from which to read the ISO 19139 XML file
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

        self.baseURI = url
        return self

    def toDCAT(self):
        """
        Converts an ISDEDatasetMetadata object to a W3C Data Catlog Vocabulary model
        
        Returns:
            A `rdflib.Graph` of the ISDEDatasetMetadata object serialised as a W3C
            Data Catalog Vocabulary (DCAT) Dataset
        """
        g = Graph()
        g.bind(ISDERDFNamespaces.DCAT['ns'], ISDERDFNamespaces.DCAT['url'])
        g.bind(ISDERDFNamespaces.DCT['ns'], ISDERDFNamespaces.DCT['url'])
        g.bind(ISDERDFNamespaces.RDFS['ns'], ISDERDFNamespaces.RDFS['url'])

        g.add((URIRef(self.baseURI), URIRef(ISDERDFNamespaces.RDFS['url'] + 'type'),
               URIRef(ISDERDFNamespaces.DCAT['url'] + 'Dataset')))
        if self.title is not None:
            g.add((URIRef(self.baseURI), URIRef(ISDERDFNamespaces.DCT['url'] + 'title'), Literal(self.title)))
        if self.abstract is not None:
            g.add((URIRef(self.baseURI), URIRef(ISDERDFNamespaces.DCT['url'] + 'description'), Literal(self.abstract)))
        if self.identifier is not None:
            g.add((URIRef(self.baseURI), URIRef(ISDERDFNamespaces.DCT['url'] + 'identifier'), Literal(self.identifier)))
        if self.dateIssued is not None:
            g.add((URIRef(self.baseURI), URIRef(ISDERDFNamespaces.DCT['url'] + 'issued'), Literal(self.dateIssued)))
        if self.keywords is not None:
            for kws in self.keywords:
                for kw in kws.keyword:
                    g.add((URIRef(self.baseURI), URIRef(ISDERDFNamespaces.DCAT['url'] + 'keyword'),
                           Literal(kw.name)))

        for topic in self.topicCategories:
            g.add((URIRef(self.baseURI), URIRef(ISDERDFNamespaces.DCAT['url'] + 'theme'), Literal(topic)))

        return g

    def toSchemaOrg(self):
        """
        Converts an ISDEDatasetMetadata object to a Schema.org graph model
        
        Returns:
            A `rdflib.Graph` of the ISDEDatasetMetadata object serialised as a
            Schema.org Dataset
        """
        g = Graph()

        if self.title is not None:
            g.add((URIRef(self.baseURI), URIRef(ISDERDFNamespaces.SDO['url'] + 'name'), Literal(self.title)))
        if self.abstract is not None:
            g.add((URIRef(self.baseURI), URIRef(ISDERDFNamespaces.SDO['url'] + 'description'), Literal(self.abstract)))
        if self.identifier is not None:
            g.add((URIRef(self.baseURI), URIRef(ISDERDFNamespaces.SDO['url'] + 'identifier'), Literal(self.identifier)))
        if self.dateIssued is not None:
            g.add((URIRef(self.baseURI), URIRef(ISDERDFNamespaces.SDO['url'] + 'datePublished'),
                   Literal(self.dateIssued)))
        if self.keywords is not None:
            for kws in self.keywords:
                for kw in kws.keyword:
                    if kw.url is not None:
                        g.add((URIRef(self.baseURI), URIRef(ISDERDFNamespaces.SDO['url'] + 'keywords'),
                               URIRef(kw.url)))
                        g.add((URIRef(kw.url), URIRef(ISDERDFNamespaces.RDFS['url'] + 'type'),
                               URIRef(ISDERDFNamespaces.SDO['url'] + 'DefinedTerm')))
                    if kw.name is not None:
                        g.add((URIRef(kw.url), URIRef(ISDERDFNamespaces.SDO['url'] + 'name'),
                               Literal(kw.name)))
                    if kws.thesaurus['url'] is not None:
                        g.add((URIRef(kw.url), URIRef(ISDERDFNamespaces.SDO['url'] + 'inDefinedTermSet'),
                               Literal(kws.thesaurus['url'])))
                        g.add((URIRef(kws.thesaurus['url']), URIRef(ISDERDFNamespaces.RDFS['url'] + 'type'),
                               URIRef(ISDERDFNamespaces.SDO['url'] + 'DefinedTermSet')))
                    if kws.thesaurus['title'] is not None:
                        g.add((URIRef(kws.thesaurus['url']), URIRef(ISDERDFNamespaces.SDO['url'] + 'name'),
                               Literal(kws.thesaurus['title'])))
        for topic in self.topicCategories:
            g.add((URIRef(self.baseURI), URIRef(ISDERDFNamespaces.SDO['url'] + 'keywords'), Literal(topic)))
        return g
