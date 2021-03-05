/*
 * Copyright 2021 Irish Spatial Data Exchange.
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *      http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
package ie.isde.metadata;

import com.github.mustachejava.DefaultMustacheFactory;
import com.github.mustachejava.MustacheFactory;
import com.github.mustachejava.Mustache;

import java.io.StringWriter;

import java.util.ArrayList;
import java.util.List;

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
    
    private String baseURI;
    private String dateIssued;
    private String fileIdentifier;
    private String metadataAbstract;
    private String title;
    
    private Document document;
    private final List<KeywordCollection> kws;
    public final List<ThemeCollection> theme;
    public final List<VariableMeasuredCollection> variableMeasured;
    private Model model;
    private Resource graphRoot;
    private XPath xPath;
    
    public Dataset(){
        this.setModel(ModelFactory.createDefaultModel());
        this.kws = new ArrayList<>();
        this.theme = new ArrayList<>();
        this.variableMeasured = new ArrayList<>();
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
            this.isoExtractFileIdentifier();
            this.isoExtractDataIssued();
            this.isoExtractKeywords();
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
    @Override
    public String fileIdentifier(){ return this.fileIdentifier; }
    @Override
    public String identifierToFileName(){ return ""; };
    @Override
    public String dateIssued(){ return this.dateIssued; }
    public List<KeywordCollection> keywordCollection(){ return this.kws; };
    
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
 /*
  Add the file identifier to the graph
*/    
        P = m.createProperty(RDFNamespaces.SDO.nsURI() + "identifier");
        L = m.createLiteral(this.fileIdentifier());
        m.add(this.graphRoot(),P,L);
/*
  Add the date issued to the graph
*/    
        try{
            P = m.createProperty(RDFNamespaces.SDO.nsURI() + "datePublished");
            L = m.createLiteral(this.dateIssued());
            m.add(this.graphRoot(),P,L);
        } catch (Exception e) {}
    
/*
  Add keywords to the graph        
*/
        List<KeywordCollection> kwcs = this.keywordCollection();
        KeywordCollection kc;
        Keyword kw;
        Resource bN;
        Resource bNN;
        
        for (int i = 0; i < kwcs.size(); i++) {
            kc = kwcs.get(i);
            List<Keyword> kwds = kc.keyword;
            for (int j = 0; j < kwds.size(); j++) {
                kw = kwds.get(j);
                
                try{
                    bN = m.createResource(kw.url);
                } catch ( java.lang.NullPointerException e ){
                    bN = m.createResource();
                }
                
                try{
                    P = m.createProperty(RDFNamespaces.SDO.nsURI() + "keywords");
                    m.add(this.graphRoot(),P,bN);
                } catch ( java.lang.NullPointerException e ){}
                
                try{
                    P = m.createProperty(RDFNamespaces.RDFS.nsURI() + "type");
                    O = m.createProperty(RDFNamespaces.SDO.nsURI() + "DefinedTerm");
                    m.add(bN,P,O);
                } catch ( java.lang.NullPointerException e ){}
                
                try{
                    P = m.createProperty(RDFNamespaces.SDO.nsURI() + "name");
                    L = m.createLiteral(kw.preferredLabel);
                    m.add(bN,P,L);
                } catch ( java.lang.NullPointerException e ){} 
                
                try{
                    bNN = m.createResource(kc.url);
                } catch ( java.lang.NullPointerException e ){
                    bNN = m.createResource();
                }
                
                P = m.createProperty(RDFNamespaces.SDO.nsURI() + "inDefinedTermSet");
                m.add(bN,P,bNN);
                
                P = m.createProperty(RDFNamespaces.RDFS.nsURI() + "type");
                O = m.createProperty(RDFNamespaces.SDO.nsURI() + "DefinedTermSet");
                m.add(bNN,P,O);
                
                try{
                    P = m.createProperty(RDFNamespaces.SDO.nsURI() + "name");
                    L = m.createLiteral(kc.title);
                    m.add(bNN,P,L);
                } catch ( java.lang.NullPointerException e  ){}
                
                try{
                    P = m.createProperty(RDFNamespaces.SDO.nsURI() + "url");
                    L = m.createLiteral(kc.url);
                    m.add(bNN,P,L);
                } catch ( java.lang.NullPointerException e  ){}
                
            }
        }
/*
  Add themes to the graph        
*/
        List<ThemeCollection> tcs = this.theme;
        
        for (int i = 0; i < tcs.size(); i++) {
            kc = tcs.get(i);
            List<Keyword> kwds = kc.keyword;
            for (int j = 0; j < kwds.size(); j++) {
                kw = kwds.get(j);
                
                try{
                    bN = m.createResource(kw.url);
                } catch ( java.lang.NullPointerException e ){
                    bN = m.createResource();
                }
                
                try{
                    P = m.createProperty(RDFNamespaces.SDO.nsURI() + "keywords");
                    m.add(this.graphRoot(),P,bN);
                } catch ( java.lang.NullPointerException e ){}
                
                try{
                    P = m.createProperty(RDFNamespaces.RDFS.nsURI() + "type");
                    O = m.createProperty(RDFNamespaces.SDO.nsURI() + "DefinedTerm");
                    m.add(bN,P,O);
                } catch ( java.lang.NullPointerException e ){}
                
                try{
                    P = m.createProperty(RDFNamespaces.SDO.nsURI() + "name");
                    L = m.createLiteral(kw.preferredLabel);
                    m.add(bN,P,L);
                } catch ( java.lang.NullPointerException e ){} 
                
                try{
                    bNN = m.createResource(kc.url);
                } catch ( java.lang.NullPointerException e ){
                    bNN = m.createResource();
                }
                
                P = m.createProperty(RDFNamespaces.SDO.nsURI() + "inDefinedTermSet");
                m.add(bN,P,bNN);
                
                P = m.createProperty(RDFNamespaces.RDFS.nsURI() + "type");
                O = m.createProperty(RDFNamespaces.SDO.nsURI() + "DefinedTermSet");
                m.add(bNN,P,O);
                
                try{
                    P = m.createProperty(RDFNamespaces.SDO.nsURI() + "name");
                    L = m.createLiteral(kc.title);
                    m.add(bNN,P,L);
                } catch ( java.lang.NullPointerException e  ){}
                
                try{
                    P = m.createProperty(RDFNamespaces.SDO.nsURI() + "url");
                    L = m.createLiteral(kc.url);
                    m.add(bNN,P,L);
                } catch ( java.lang.NullPointerException e  ){}
            }
        }
        
        /*
  Add variables measured to the graph        
*/
        List<VariableMeasuredCollection> vmc = this.variableMeasured;
        Resource vM;
        
        for (int i = 0; i < vmc.size(); i++) {
            kc = vmc.get(i);
            List<Keyword> kwds = kc.keyword;
            for (int j = 0; j < kwds.size(); j++) {
                kw = kwds.get(j);
                vM = m.createResource();
                
                P = m.createProperty(RDFNamespaces.SDO.nsURI() + "variableMeasured");
                m.add(this.graphRoot(),P,vM);
                
                P = m.createProperty(RDFNamespaces.RDFS.nsURI() + "type");
                O = m.createProperty(RDFNamespaces.SDO.nsURI() + "PropertyValue");
                m.add(vM,P,O);
                
                try{
                    P = m.createProperty(RDFNamespaces.SDO.nsURI() + "name");
                    L = m.createLiteral(kw.preferredLabel);
                    m.add(vM,P,L);
                } catch (Exception e) {}
                
                try{
                    P = m.createProperty(RDFNamespaces.SDO.nsURI() + "url");
                    L = m.createLiteral(kw.url);
                    m.add(vM,P,L);
                } catch (Exception e) {}
            }
        }
        
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
        Literal L;
        try {
            P = m.createProperty(RDFNamespaces.DCT.nsURI() + "title");
            L = m.createLiteral(this.title());
            m.add(this.graphRoot(),P,L);
        } catch(Exception e){}
/*
  Add the Dataset abstract to the graph
*/    
        try {
            P = m.createProperty(RDFNamespaces.DCT.nsURI() + "description");
            L = m.createLiteral(this.metadataAbstract());
            m.add(this.graphRoot(),P,L);
        } catch (Exception e){ }
/*
  Add the file identifier to the graph
*/    
        try {
            P = m.createProperty(RDFNamespaces.DCT.nsURI() + "identifier");
            L = m.createLiteral(this.fileIdentifier());
            m.add(this.graphRoot(),P,L);
        } catch (Exception e){ }
/*
  Add the date issued to the graph
*/    
        try {
            P = m.createProperty(RDFNamespaces.DCT.nsURI() + "issued");
            L = m.createLiteral(this.dateIssued());
            m.add(this.graphRoot(),P,L);
        } catch (Exception e){ }
/*
  Add keywords to the graph        
*/
        List<KeywordCollection> kwcs = this.keywordCollection();
        KeywordCollection kc;
        Keyword kw;
        
        for (int i = 0; i < kwcs.size(); i++) {
            kc = kwcs.get(i);
            List<Keyword> kwds = kc.keyword;
            for (int j = 0; j < kwds.size(); j++) {
                kw = kwds.get(j);
                
                try{
                    P = m.createProperty(RDFNamespaces.DCAT.nsURI() + "keyword");
                    L = m.createLiteral(kw.preferredLabel);
                    m.add(this.graphRoot(),P,L);
                } catch (Exception e) {}
            }
        }
/*
  Add variables measured to the graph        
*/
        List<VariableMeasuredCollection> vmc = this.variableMeasured;
        
        for (int i = 0; i < vmc.size(); i++) {
            kc = vmc.get(i);
            List<Keyword> kwds = kc.keyword;
            for (int j = 0; j < kwds.size(); j++) {
                kw = kwds.get(j);
                
                try{
                    P = m.createProperty(RDFNamespaces.DCAT.nsURI() + "keyword");
                    L = m.createLiteral(kw.preferredLabel);
                    m.add(this.graphRoot(),P,L);
                } catch (Exception e) {}
            }
        }
/*
  Add themes to the graph
*/
/*
  Add variables measured to the graph        
*/
        List<ThemeCollection> tc = this.theme;
        Resource tcN;
        Resource kwN;
        
        for (int i = 0; i < tc.size(); i++) {
            kc = tc.get(i);
            tcN = m.createResource(kc.url);
            List<Keyword> kwds = kc.keyword;
            for (int j = 0; j < kwds.size(); j++) {
                kw = kwds.get(j);
                kwN = m.createResource(kw.url);
                
                P = m.createProperty(RDFNamespaces.DCAT.nsURI() + "theme");
                m.add(this.graphRoot(),P,kwN);
                
                P = m.createProperty(RDFNamespaces.RDFS.nsURI() + "type");
                O = m.createProperty(RDFNamespaces.SKOS.nsURI() + "Concept");
                m.add(kwN,P,O);
                
                P = m.createProperty(RDFNamespaces.SKOS.nsURI() + "inScheme");
                m.add(kwN,P,tcN);
                
                P = m.createProperty(RDFNamespaces.RDFS.nsURI() + "type");
                O = m.createProperty(RDFNamespaces.SKOS.nsURI() + "ConceptScheme");
                m.add(tcN,P,O);
                
                try{
                    P = m.createProperty(RDFNamespaces.SKOS.nsURI() + "prefLabel");
                    L = m.createLiteral(kw.preferredLabel);
                    m.add(kwN,P,L);
                } catch (Exception e) {}
                
                try{
                    P = m.createProperty(RDFNamespaces.SKOS.nsURI() + "prefLabel");
                    L = m.createLiteral(kc.title);
                    m.add(tcN,P,L);
                } catch (Exception e) {}
            }
        }
/*
  Add RDF namesaces to the graph
*/
        m.setNsPrefix(RDFNamespaces.DCT.ns(), RDFNamespaces.DCT.nsURI());
        m.setNsPrefix(RDFNamespaces.DCAT.ns(), RDFNamespaces.DCAT.nsURI());
        m.setNsPrefix(RDFNamespaces.RDFS.ns(), RDFNamespaces.RDFS.nsURI());
        m.setNsPrefix(RDFNamespaces.SKOS.ns(), RDFNamespaces.SKOS.nsURI());
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
    private void appendKeywordCollection(KeywordCollection kc){ this.kws.add(kc); }
    
    private void setBaseUri(String baseUri){ this.baseURI = baseUri; }
    private void setDocument(Document doc){ this.document = doc; }
    private void setFileIdentifier(String fileIdentifier){ this.fileIdentifier = fileIdentifier; }
    private void setGraphRoot( Resource graphRoot ){ this.graphRoot = graphRoot; }
    private void setMetadataAbstract(String mAbstract){ this.metadataAbstract = mAbstract; };
    private void setModel(Model model){ this.model = model; }
    private void setTitle(String title){ this.title = title; }
    private void setXPath(XPath xPath){ this.xPath = xPath; }
    private void setDateIssued(String date){ this.dateIssued = date; }
/*
   Methods for extracting metdata from ISO XML using XPath expressions
 */ 
    private void isoExtractAbstract() throws javax.xml.xpath.XPathException{
        NodeList nodeList = (NodeList) this.xPath().compile(IsoXmlQueries.ABSTRACT.xPath()).evaluate(
                                      this.document(), XPathConstants.NODESET);
            for (int i = 0; i < nodeList.getLength(); i++) {
                Node currentItem = nodeList.item(i);
                this.setMetadataAbstract(currentItem.getTextContent().trim().replace("\n", "").replace("\r", ""));
            }
    }
    
    private void isoExtractFileIdentifier() throws javax.xml.xpath.XPathException{
        NodeList nodeList = (NodeList) this.xPath().compile(IsoXmlQueries.FILEIDENTIFIER.xPath()).evaluate(
                                      this.document(), XPathConstants.NODESET);
            for (int i = 0; i < nodeList.getLength(); i++) {
                Node currentItem = nodeList.item(i);
                this.setFileIdentifier(currentItem.getTextContent().trim());
            }
    }
    
    private void isoExtractTitle() throws javax.xml.xpath.XPathException{
        NodeList nodeList = (NodeList) this.xPath().compile(IsoXmlQueries.TITLE.xPath()).evaluate(
                                      this.document(), XPathConstants.NODESET);
            for (int i = 0; i < nodeList.getLength(); i++) {
                Node currentItem = nodeList.item(i);
                this.setTitle(currentItem.getTextContent().trim());
            }
    }
    
    private void isoExtractDataIssued() throws javax.xml.xpath.XPathException{
        NodeList nodeList = (NodeList) this.xPath().compile(IsoXmlQueries.DATEISSUED.xPath()).evaluate(
                                      this.document(), XPathConstants.NODESET);
            for (int i = 0; i < nodeList.getLength(); i++) {
                Node currentItem = nodeList.item(i);
                this.setDateIssued(currentItem.getTextContent().trim());
            }
    }
    
    private void isoExtractKeywords() throws javax.xml.xpath.XPathException,
                                javax.xml.parsers.ParserConfigurationException {
        KeywordCollection kc;
        DocumentBuilderFactory dbf = DocumentBuilderFactory.newInstance();
        DocumentBuilder db = dbf.newDocumentBuilder();
        Document doc;
        String sNode;
        NodeList titleList;
        String handlingRule;
        
        NodeList nodeList = (NodeList) this.xPath().compile(IsoXmlQueries.KEYWORDGROUP.xPath()).evaluate(
                                      this.document(), XPathConstants.NODESET);
        for (int i = 0; i < nodeList.getLength(); i++) {
            handlingRule = "";
            
            Node currentItem = nodeList.item(i);
            sNode = currentItem.toString();
            
            doc = db.newDocument();
            Node iN = doc.importNode(currentItem,true);
            doc.appendChild(iN);
            
            titleList = (NodeList) this.xPath().compile(IsoXmlQueries.THESAURUSNAME.xPath()).evaluate(
                                      doc, XPathConstants.NODESET);
            
            try {
                for (KeywordCollectionHandlingRules kchr : KeywordCollectionHandlingRules.values()) { 
                    if(titleList.item(0).getTextContent().trim().equals(kchr.keywordCollectionName)){
                        handlingRule = kchr.rule;
                    }
                }
            } catch (Exception ee){}
            
            switch(handlingRule){
                case "theme":
                    this.theme.add(new ThemeCollection(doc));
                    break;
                case "variableMeasured":
                    this.variableMeasured.add(new VariableMeasuredCollection(doc));
                    break;
                case "ignore":
                    break;
                default:
                    kc = new KeywordCollection(doc);
                    this.appendKeywordCollection(kc);
            }
        }
    }
    
    @Override
    public String toString()  {
        MustacheFactory mf = new DefaultMustacheFactory();
        Mustache mustache = mf.compile("toString__Dataset.mustache");
        
        StringWriter sw = new StringWriter();
        
        try {
            mustache.execute(sw, this).flush();
        } catch(java.io.IOException e) {}
        
        return sw.toString();
    }
}
