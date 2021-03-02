/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package ie.isde.metadata;

/**
 * Enumerates the RDF namespaces required for the translated Irish Spatial Data
 * Exchange metadata
 * 
 * @author Adam Leadbetter
 * @version 1.0
 * @since 1.0
 */
public enum RDFNamespaces {
    DCT ("dct", "http://purl.org/dc/terms/"),
    /**
     * World Wide Web Consortium Data Catalog vocabulary
     */
    DCAT ("dcat", "http://www.w3.org/ns/dcat#"),
    /**
     * RDF Schema vocabulary
     */
    RDFS ("rdfs", "http://www.w3.org/1999/02/22-rdf-syntax-ns#"),
    /**
     * Schema,org vocabulary
     */
    SDO ("sdo", "https://schema.org/");
    
    private final String preferredNamespace;
    private final String uri;
    
    RDFNamespaces(String preferredNamespace, String uri){
        this.preferredNamespace = preferredNamespace;
        this.uri = uri;
    }
    /**
     * Get the preferred namespace prefix for the vocabulary
     * 
     * @return  String   The preferred namespace prefix for the vocabulary
     */
    public String ns(){return this.preferredNamespace;}
    /**
     * Get the preferred namespace URI for the vocabulary
     * 
     * @return  String   The preferred namespace URI for the vocabulary
     */
    public String nsURI(){return this.uri;}
}
