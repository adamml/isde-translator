/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package ie.isde.metadata.translator;

/**
 * IsoBase provides an interface to specify the public facing class for 
 * translating ISO19115/19139 metadata to other representations.
 * 
 * @author Adam Leadbetter
 * @version 1.0
 * @since 1.0
 */

public interface ITranslator {
    /**
     * Translates the Irish Spatial Data Exchange metadata record supplied in
     * ISO19115/19139 XML to a W3C Data Catalog Vocabulary representation
     * 
     * @return String   The DCAT representation of the ISO metadata as a Terse
     *                  Triple Language serialization
     * @version 1.0
     * @since 1.0
     */
    public String toDCAT();
    /**
     * Translates the Irish Spatial Data Exchange metadata record supplied in
     * ISO19115/19139 XML to a Schema.org representation
     * 
     * @return String   The Schema.org representation of the ISO metadata as a 
     *                  JSON-LD serialization
     */
    public String toSchemaOrg();
}
