import urllib.request

from owslib.iso import MD_Metadata, etree

from .ISDERDFNamespaces import ISDERDFNamespaces

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
        populates the ISDEDatasetMetadata class attributes appropiately.
        
        Args:
            url: A string representing the URL from which to read the ISO 19139 XML file
        """
        with urllib.request.urlopen(url) as metadata:
            md = MD_Metadata(etree.parse(metadata))
        # Extract Title
            try:
                self.title = md.identification.title
            except:
                pass
        # Extract Abstract
            try:
                self.abstract = md.identification.abstract
            except:
                pass
        # Extract Identifier
            try:
                self.identifier = md.identifier
            except:
                pass
        # Extract Topic Categories
            try:
                self.topicCategories = md.identification.topiccategory
            except:
                pass
        # Extract the Date Issued
            try:
                self.dateIssued = md.datestamp
            except:
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
        g.bind(ISDERDFNamespaces.DCAT['ns'],ISDERDFNamespaces.DCAT['url'])
        g.bind(ISDERDFNamespaces.DCT['ns'],ISDERDFNamespaces.DCT['url'])
        g.bind(ISDERDFNamespaces.RDFS['ns'],ISDERDFNamespaces.RDFS['url'])
        
        g.add((URIRef(self.baseURI),URIRef(ISDERDFNamespaces.RDFS['url']+'type'),URIRef(ISDERDFNamespaces.DCAT['url'] + 'Dataset')))
        if self.title is not None:
            g.add((URIRef(self.baseURI),URIRef(ISDERDFNamespaces.DCT['url']+'title'),Literal(self.title)))
        if self.abstract is not None:
            g.add((URIRef(self.baseURI),URIRef(ISDERDFNamespaces.DCT['url']+'description'),Literal(self.abstract)))
        if self.identifier is not None:
            g.add((URIRef(self.baseURI),URIRef(ISDERDFNamespaces.DCT['url']+'identifier'),Literal(self.identifier)))
        if self.dateIssued is not None:
            g.add((URIRef(self.baseURI),URIRef(ISDERDFNamespaces.DCT['url']+'issued'),Literal(self.dateIssued)))
        
        for topic in self.topicCategories:
            g.add((URIRef(self.baseURI),URIRef(ISDERDFNamespaces.DCAT['url']+'theme'),Literal(topic)))
        
        return g
    
    def toSchemaOrg(self):
        """
        Converts an ISDEDatasetMetadata object to a Schma.org graph model
        
        Returns:
            A `rdflib.Graph` of the ISDEDatasetMetadata object serialised as a
            Schema.org Dataset
        """
        g = Graph()
        
        if self.title is not None:
            g.add((URIRef(self.baseURI),URIRef(ISDERDFNamespaces.SDO['url']+'name'),Literal(self.title)))
        if self.abstract is not None:
            g.add((URIRef(self.baseURI),URIRef(ISDERDFNamespaces.SDO['url']+'description'),Literal(self.abstract)))
        if self.identifier is not None:
            g.add((URIRef(self.baseURI),URIRef(ISDERDFNamespaces.SDO['url']+'identifier'),Literal(self.identifier)))
        if self.dateIssued is not None:
            g.add((URIRef(self.baseURI),URIRef(ISDERDFNamespaces.SDO['url']+'datePublished'),Literal(self.dateIssued)))
        
        for topic in self.topicCategories:
            g.add((URIRef(self.baseURI),URIRef(ISDERDFNamespaces.SDO['url']+'keywords'),Literal(topic)))
        return g