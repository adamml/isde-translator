/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package ie.isde.metadata;

import org.apache.jena.rdf.model.*;

/**
 * This interface is used for all base metadata entity types within the Irish 
 * Spatial Data Exchange system
 * 
 * @author Adam Leadbetter
 */
public interface Metadata {
     /**
     * Translates the Irish Spatial Data Exchange metadata record supplied in
     * ISO19115/19139 XML to a W3C Data Catalog Vocabulary representation
     * 
     * @return String   The DCAT representation of the ISO metadata as a Terse
     *                  Triple Language serialization
     * @version 1.0
     * @since 1.0
     */
    public Model toDCAT();
    /**
     * Translates the Irish Spatial Data Exchange metadata record supplied in
     * ISO19115/19139 XML to a Schema.org representation
     * 
     * @return String   The Schema.org representation of the ISO metadata as a 
     *                  JSON-LD serialization
     */
    public Model toSchemaOrg();
}
