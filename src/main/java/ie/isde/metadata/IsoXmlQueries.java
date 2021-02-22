/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package ie.isde.metadata;

/**
 *
 * Enumerates the XPath queries used to extract the various metadata attributes
 * used in a constructing a Dataset object 
 * 
 * @author Adam Leadbetter
 */
public enum IsoXmlQueries {
    /**
     * Extract a metadata abstract from an ISO 19139 record
     */
    ABSTRACT ("//*[self::abstract]"),
    /**
     * Extract the title from an ISO 19139 record
     */
    TITLE ("//*[self::identificationInfo]//*[self::MD_DataIdentification]//*[self::citation]//*[self::CI_Citation]//*[self::title]");
    
    private final String xPath;
    /**
     * Get the enumerator XPath query for the ENUM value
     * 
     * @param xPath     The XPath query as a String
     */
    IsoXmlQueries(String xPath){
        this.xPath = xPath;
    }
    
    public String xPath(){ return this.xPath; }
}
