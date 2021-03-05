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

/**
 * A number of KeywordCollections should be used for more specialised purposes,
 * including ThemeCollections and VariableMeasuredCollections. ISO19139 XML,
 * the W3C Data Catalog Vocabulary and Schema.org do not all handle these 
 * distinctions well. This Enum allows control over some of these 
 * specialisations.
 * 
 * Some KeywordCollections used in ISO19139 may also require being ignored for
 * other serialisation types.
 * 
 * @author Adam Leadbetter
 */
public enum KeywordCollectionHandlingRules {
    /**
     * BODC Parameter Usage Vocabulary - VariableMeasuredCollection
     */
    P01("BODC Parameter Usage Vocabulary","http://vocab.nerc.ac.uk/collection/P01/current/","variableMeasured"),
    /**
     * ISO Topic Categories published on the NERC Vocabulary Server - 
     * ThemeCollection
     */
    ISOTOPICSONNVS("International Standards Organisation ISO19115 Topic Categories","http://vocab.nerc.ac.uk/collection/P05/current/","theme"),
    /**
     * GEMET Version 1.0 INSPIRE Themes published on the NERC Vocabulary Server 
     * - Theme Collection 
     */
    GEMETINSPIREONNVS("GEMET - INSPIRE themes, version 1.0","http://vocab.nerc.ac.uk/collection/P22/current/","theme"),
    /**
     * GEMET INSPIRE Theme Tile Case - Theme Collection
     */
    GEMETINSPIRETHEMETITLECASE("GemetInspireTheme","","theme"),
    /**
     * Marine Institute Calendar Concept Scheme - ignore
     */
    MARINEINSTITUTECALENDAR("Marine Institute Calendar Concept Scheme","http://linked.marine.ie/calendar","ignore");
    
    /**
     * The lexical name of this KeywordCollection as a String
     */
    public final String keywordCollectionName;
    /**
     * The URL to this KeywordCollection as a String
     */
    public final String keywordCollecionUrl;
    /**
     * The handling rule for this KeywordCollection as a String. Valid rules 
     * are:
     * 
     *      - ignore                Do nothing with this KeywordCollection
     * 
     *      - theme                 Handle this KeywordCollection as a 
     *                              ThemeCollection
     * 
     *      - variableMeasured      Handle this KeywordCollection as a
     *                              VariableMeasuredCollection     * 
     */
    public final String rule;
    
    KeywordCollectionHandlingRules(String kCN, String kCU, String r){
        this.keywordCollectionName = kCN;
        this.keywordCollecionUrl = kCU;
        switch(r.toLowerCase()){
            case "ignore":
                break;
            case "variablemeasured":
                break;
            case "theme":
                break;
            default:
                throw new java.lang.IllegalArgumentException(
                    "Invalid KeywordCollectionHandlingRules rule supplied [" + r + "]...");
        }
            this.rule =  r;
    }
}
