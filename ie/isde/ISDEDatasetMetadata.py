import urllib.request

import xml.etree.ElementTree

from .Namespaces import ISDERDFNamespaces, ISDEXMLNamespaces 
from .ISDEDatasetParser import ISDEDatasetParser

from rdflib import Graph, URIRef, Literal

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
    The date on which the metadta record was issued
    """
    identifier: str = None
    """
    A unique identifier to this Dataset object
    """
    title: str = None
    """
    The lexical title of the Dataset object
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
            e = xml.etree.ElementTree.parse(metadata).getroot()
            self.title = str(e.findall(ISDEDatasetParser.TITLE,ISDEXMLNamespaces.NAMESPACES)[0].text)
            self.abstract = str(e.findall(ISDEDatasetParser.ABSTRACT,ISDEXMLNamespaces.NAMESPACES)[0].text)
            self.identifier = str(e.findall(ISDEDatasetParser.IDENTIFIER,ISDEXMLNamespaces.NAMESPACES)[0].text)
            self.dateIssued = str(e.findall(ISDEDatasetParser.DATEISSUED,ISDEXMLNamespaces.NAMESPACES)[0].text)
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
        g.add((URIRef(self.baseURI),URIRef(ISDERDFNamespaces.DCT['url']+'title'),Literal(self.title)))
        g.add((URIRef(self.baseURI),URIRef(ISDERDFNamespaces.DCT['url']+'description'),Literal(self.abstract)))
        g.add((URIRef(self.baseURI),URIRef(ISDERDFNamespaces.DCT['url']+'identifier'),Literal(self.identifier)))
        
        return g
    
    def toSchemaOrg(self):
        """
        Converts an ISDEDatasetMetadata object to a Schma.org graph model
        
        Returns:
            A `rdflib.Graph` of the ISDEDatasetMetadata object serialised as a
            Schema.org Dataset
        """
        g = Graph()
        
        g.add((URIRef(self.baseURI),URIRef(ISDERDFNamespaces.SDO['url']+'name'),Literal(self.title)))
        g.add((URIRef(self.baseURI),URIRef(ISDERDFNamespaces.SDO['url']+'description'),Literal(self.abstract)))
        g.add((URIRef(self.baseURI),URIRef(ISDERDFNamespaces.SDO['url']+'identifier'),Literal(self.identifier)))
        
        return g