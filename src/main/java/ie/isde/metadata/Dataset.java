/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package ie.isde.metadata;

import javax.xml.parsers.DocumentBuilder;
import javax.xml.parsers.DocumentBuilderFactory;
import javax.xml.xpath.XPath;
import javax.xml.xpath.XPathFactory;
import javax.xml.xpath.XPathConstants;

import org.w3c.dom.Document;
import org.w3c.dom.Node;
import org.w3c.dom.NodeList;

import org.apache.jena.rdf.model.*;

/**
 * Implements the Dataset Interface to create objects of the Dataset type to
 * represent metadata objects of this type within the Irish Spatial Data 
 * Exchange.
 * 
 * @author Adam Leadbetter
 */
public class Dataset implements IDataset, Metadata {
    
    private String metadataAbstract;
    private String baseURI;
    private Document document;
    private String title;
    private Model model;
    private XPath xPath;
    private Resource graphRoot;
    
    public Dataset(){
        this.setModel(ModelFactory.createDefaultModel());
    }
    
    @Override
    public void fromISO(String isoLocator)
                    throws javax.xml.parsers.ParserConfigurationException,
                           org.xml.sax.SAXException,
                           java.io.IOException,
                           javax.xml.xpath.XPathException {
    
        Document d = null;
/*
   Load from a remote URL
 */
        if(isoLocator.contains("http://") ||
                                            isoLocator.contains("https://") ||
                                            isoLocator.contains("ftp://"))
        {
            DocumentBuilderFactory dbf = DocumentBuilderFactory.newInstance();
            DocumentBuilder dBuilder = dbf.newDocumentBuilder();
            d = dBuilder.parse(isoLocator);
            this.setDocument(d);
/*
  Extract the relevant information from the ISO XML document
*/
            this.setXPath(XPathFactory.newInstance().newXPath());
            this.isoExtractTitle();
            this.isoExtractAbstract();
/*
   Set the base URI from the URI read
 */
            this.setBaseUri(isoLocator);
/*
   Set the Resource for the root of the RDF graph for this metadata object
 */
            this.setGraphRoot(this.model().createResource(this.baseUri()));
        } else {
        
        }
    }
/*
   Public get methods
*/
    @Override
    public String metadataAbstract() { return this.metadataAbstract; };
    @Override
    public String baseUri(){ return this.baseURI; };
    @Override
    public String title(){ return this.title; }
/*
  Public translator methods  
*/
    @Override
    public Model toSchemaOrg(){ 
        Model m = this.model();
/*
  The entity is of RDFS type sdo:Dataset
*/ 
        Property P = 
                    m.createProperty( RDFNamespaces.RDFS.nsURI() + "type" );
        Property O = 
                    m.createProperty( RDFNamespaces.SDO.nsURI() + "Dataset" );
        m.add(this.graphRoot(), P, O);
/*
  Add the Dataset title to the graph
*/    
        P = m.createProperty(RDFNamespaces.SDO.nsURI() + "name");
        Literal L = m.createLiteral(this.title());
        m.add(this.graphRoot(),P,L);
/*
  Add the Dataset abstract to the graph
*/    
        P = m.createProperty(RDFNamespaces.SDO.nsURI() + "description");
        L = m.createLiteral(this.metadataAbstract());
        m.add(this.graphRoot(),P,L);
        return m;
    }
    @Override
    public Model toDCAT(){ 
        Model m = this.model();
/*
  The entity is of RDFS type dcat:Dataset
*/ 
        Property P = 
                    m.createProperty( RDFNamespaces.RDFS.nsURI() + "type" );
        Property O = 
                    m.createProperty( RDFNamespaces.DCAT.nsURI() + "Dataset" );
        m.add(this.graphRoot(), P, O);
/*
  Add the Dataset title to the graph
*/    
        P = m.createProperty(RDFNamespaces.DCT.nsURI() + "title");
        Literal L = m.createLiteral(this.title());
        m.add(this.graphRoot(),P,L);
/*
  Add the Dataset abstract to the graph
*/    
        P = m.createProperty(RDFNamespaces.DCT.nsURI() + "description");
        L = m.createLiteral(this.metadataAbstract());
        m.add(this.graphRoot(),P,L);
/*
  Add RDF namesaces to the graph
*/
        m.setNsPrefix(RDFNamespaces.DCT.ns(), RDFNamespaces.DCT.nsURI());
        m.setNsPrefix(RDFNamespaces.DCAT.ns(), RDFNamespaces.DCAT.nsURI());
        m.setNsPrefix(RDFNamespaces.RDFS.ns(), RDFNamespaces.RDFS.nsURI());
        return m; 
    }
/*
   Private get methods
 */
    private Document document() { return this.document; }
    private Resource graphRoot() { return this.graphRoot; }
    private Model model() { return this.model; }
    private XPath xPath() { return this.xPath; }
/*
   Set methods
 */    
    private void setBaseUri(String baseUri){ this.baseURI = baseUri; }
    private void setDocument(Document doc){ this.document = doc; }
    private void setGraphRoot( Resource graphRoot ){ this.graphRoot = graphRoot; }
    private void setMetadataAbstract(String mAbstract){ this.metadataAbstract = mAbstract; };
    private void setModel(Model model){ this.model = model; }
    private void setTitle(String title){ this.title = title; }
    private void setXPath(XPath xPath){ this.xPath = xPath; }
/*
   Methods for extracting metdata from ISO XML using XPath expressions
 */ 
    private void isoExtractAbstract() throws javax.xml.xpath.XPathException{
        NodeList nodeList = (NodeList) this.xPath().compile(IsoXmlQueries.ABSTRACT.xPath()).evaluate(
                                      this.document(), XPathConstants.NODESET);
            for (int i = 0; i < nodeList.getLength(); i++) {
                Node currentItem = nodeList.item(i);
                this.setTitle(currentItem.getTextContent().trim());
            }
    }
    
    private void isoExtractTitle() throws javax.xml.xpath.XPathException{
        NodeList nodeList = (NodeList) this.xPath().compile(IsoXmlQueries.TITLE.xPath()).evaluate(
                                      this.document(), XPathConstants.NODESET);
            for (int i = 0; i < nodeList.getLength(); i++) {
                Node currentItem = nodeList.item(i);
                this.setMetadataAbstract(currentItem.getTextContent().trim());
            }
    }
}
