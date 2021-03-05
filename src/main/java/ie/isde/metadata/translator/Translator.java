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
package ie.isde.metadata.translator;

import java.io.StringWriter;

import java.util.HashMap;
import java.util.Map;

import ie.isde.metadata.Dataset;
import ie.isde.metadata.RDFNamespaces;

import org.apache.jena.rdf.model.*;
import org.apache.jena.riot.Lang;
import org.apache.jena.riot.RDFDataMgr;

import com.github.jsonldjava.utils.JsonUtils;
import com.github.jsonldjava.core.JsonLdOptions;
import com.github.jsonldjava.core.JsonLdProcessor;

/**
 * This class facilitates different serializations of Irish Spatial Data 
 * Exchange metadata.
 * 
 * @author Adam Leadbetter
 * @version 1.0
 * @since 1.0
 */
public class Translator {
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
        
      -y      Translates the ISO XML supplied in the first argument to a 
              YAML file      

  If the flag is valid, construct an IsoTranslator =object and print the
  translation result

*/
        Dataset ds = new Dataset();
        ds.fromISO(args[0]);
        switch (args[1].toLowerCase()) {
            case "-s":
                {
                    Map context = new HashMap();
                    context.put("@vocab",RDFNamespaces.SDO.nsURI());
                    
                    Map<String, Object> frame = new HashMap<>();
                    frame.put("@type" , "Dataset");
                    frame.put("@context", context);
                    
                    StringWriter sW = new StringWriter();
                    
                    Model m = ds.toSchemaOrg();
                    RDFDataMgr.write(sW, m, Lang.JSONLD);
                    
                    Object jsonObject = JsonUtils.fromString(sW.toString());
                    
                    JsonLdOptions opts = new JsonLdOptions();
                    opts.setPruneBlankNodeIdentifiers(true);                   
                            
                    Object compact = JsonLdProcessor.frame(jsonObject, frame, opts);
                    System.out.println(JsonUtils.toPrettyString(compact));
                    
                    break;
                }
            case "-d":
                {
                    Model m = ds.toDCAT();
                    RDFDataMgr.write(System.out, m, Lang.TTL);
                    break;
                }
            case "-y":
                {
                    System.out.println(ds.toString());
                    break;
                }
            default:
                throw new java.lang.IllegalArgumentException(
                    "Target translation flag value must be either -d or -s...");
        }
    }
}
