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
import org.w3c.dom.Document;

import javax.xml.xpath.XPathConstants;
import org.w3c.dom.Node;
import org.w3c.dom.NodeList;

/**
 * Implements the Dataset Interface to create objects of the Dataset type to
 * represent metadata objects of this type within the Irish Spatial Data 
 * Exchange.
 * 
 * @author Adam Leadbetter
 */
public class Dataset implements IDataset {
    
    private String metadataAbstract;
    private String baseURI;
    private Document document;
    private String title;
    private XPath xPath;
    
    public Dataset(){}
    
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
   Private get methods
 */
    private Document document() { return this.document; };
    private XPath xPath() { return this.xPath; };
/*
   Set methods
 */    
    private void setBaseUri(String baseUri){ this.baseURI = baseUri; }
    private void setDocument(Document doc){ this.document = doc; }
    private void setMetadataAbstract(String mAbstract){ this.metadataAbstract = mAbstract; };
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
