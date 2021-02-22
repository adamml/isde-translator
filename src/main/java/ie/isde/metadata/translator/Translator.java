/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package ie.isde.metadata.translator;

import ie.isde.metadata.Dataset;

import org.apache.jena.rdf.model.*;

import org.apache.jena.riot.Lang;
import org.apache.jena.riot.RDFDataMgr;
/**
 * This class facilitates different serializations of Irish Spatial Data 
 * Exchange metadata.
 * 
 * @author Adam Leadbetter
 * @version 1.0
 * @since 1.0
 */
public class Translator implements ITranslator { //TODO: Add ecteds Dataser
/**
 * @param recordFile
 * @version 1.0
 * @since 1.0
 */    
    private Dataset dataset;
    private Model model;
    private Resource root;
    
    public Translator(String recordFile) 
                        throws java.net.MalformedURLException,
                               org.xml.sax.SAXException,
                               javax.xml.parsers.ParserConfigurationException,
                               java.io.IOException,
                               javax.xml.xpath.XPathException
    {   
        Dataset ds = new Dataset();
        ds.fromISO(recordFile);
        
        this.setDataset(ds);
        this.setModel(ModelFactory.createDefaultModel());
        this.setRoot();
    }    
/*
   Set methods 
 */
    private void setDataset(Dataset dataset){ this.dataset = dataset; }
    private void setModel(Model model){ this.model = model; }; 
    private void setRoot(){ this.root = this.model().createResource(this.dataset().baseUri()); }
    
/*
   Get methods
 */ 
    private Dataset dataset(){ return this.dataset; }
    private Model model(){ return this.model; }
    private Resource root(){ return this.root; }

    
    @Override
    public String toDCAT(){
/*
  The entity is of RDFS type dcat:Dataset
 */ 
        this.setModel(ModelFactory.createDefaultModel());
        Model m = this.model();
        Property P = 
                    m.createProperty( RDFNamespaces.RDFS.nsURI() + "type" );
        Property O = 
          m.createProperty( RDFNamespaces.DCAT.nsURI() + "Dataset" );
        m.add(this.root(), P, O);
        this.setModel(m);
        this.getTitle("-d");
        this.getAbstract("-d");
        m = this.model();
        m.setNsPrefix(RDFNamespaces.DCT.ns(), RDFNamespaces.DCT.nsURI());
        m.setNsPrefix(RDFNamespaces.DCAT.ns(), RDFNamespaces.DCAT.nsURI());
        m.setNsPrefix(RDFNamespaces.RDFS.ns(), RDFNamespaces.RDFS.nsURI());
        RDFDataMgr.write(System.out, m, Lang.TTL);
        return "";
    } 
    
    @Override
    public String toSchemaOrg(){
        this.setModel(ModelFactory.createDefaultModel());
        return "";
    }
    
    private void getTitle(String flag){
        Model m = this.model();
        Resource r = this.root();
        switch(flag){
            case "-d":{
                Property p = 
                    m.createProperty(RDFNamespaces.DCT.nsURI() + "title");
                Literal o =
                    m.createLiteral(this.dataset().title());
                m.add(r,p,o);
                break;
            }
        }
        this.setModel(m);
    }
    
     private void getAbstract(String flag){
        Model m = this.model();
        Resource r = this.root();
        switch(flag){
            case "-d":{
                Property p = 
                    m.createProperty(RDFNamespaces.DCT.nsURI() + "abstract");
                Literal o =
                    m.createLiteral(this.dataset().metadataAbstract());
                m.add(r,p,o);
                break;
            }
        }
        this.setModel(m);
    }
    
/**
 * Translates an ISO XML record from the Irish Spatial Data Exchange to either
 * World Wide Web Consortium (W3C) Data Catalog Vocabulary (DCAT) profile as
 * Terse Triple Language (TTL) or Schema.org as a JSON object conforming to the
 * JSON-LD Linked Data profile.
 * 
 * @param args
 * @throws java.lang.UnsupportedOperationException
 * @throws java.lang.IllegalArgumentException 
 * @throws java.net.MalformedURLException
 * @throws org.xml.sax.SAXException
 * @throws javax.xml.parsers.ParserConfigurationException
 * @throws java.io.IOException
 * @throws javax.xml.xpath.XPathException
 * @version 1.0
 * @since 1.0
 */    
    public static void main(String[] args)
            throws java.lang.UnsupportedOperationException,
                    java.lang.IllegalArgumentException,
                    java.net.MalformedURLException,
                    org.xml.sax.SAXException,
                    javax.xml.parsers.ParserConfigurationException,
                    java.io.IOException,
                    javax.xml.xpath.XPathException
    {
/*
   Check the correct number of input arguments are supplied
 */
        if(args.length < 2) {
            throw new java.lang.UnsupportedOperationException(
                                       "Not enough input arguments suplied...");
        } else if(args.length > 2) {
            throw new java.lang.UnsupportedOperationException(
                                       "Too many input arguments suplied...");
        }
/*
  Check that the second input value is a flag. Valid flag values are:
      -d      Translates the ISO XML supplied in the first argument to W3C
              DCAT, serialized as TTL
      -s      Translates the ISO XML supplied in the first argument to a
              Schema.org compliant JSON-LD object

  If the flag is valid, construct an IsoTranslator =object and print the
  translation result

*/
        switch (args[1].toLowerCase()) {
            case "-s":
                {
                    Translator iT = new Translator(args[0]);
                    break;
                }
            case "-d":
                {
                    Translator iT = new Translator(args[0]);
                    iT.toDCAT();
                    break;
                }
            default:
                throw new java.lang.IllegalArgumentException(
                    "Target translation flag value must be either -d or -s...");
        }
    }
}
