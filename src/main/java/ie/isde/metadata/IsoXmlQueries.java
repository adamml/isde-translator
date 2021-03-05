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
    ABSTRACT("//*[self::abstract]"),
    /**
     * Extract the date the metadata were issued from an ISO 19139 record
     */
    DATEISSUED("//*[self::dateStamp]//*[self::*]"),
    /**
     * Extract the file identifier from an ISO 19139 record
     */
    FILEIDENTIFIER("//*[self::fileIdentifier]//*[self::CharacterString]"),
    /**
     * Extract a keyword preferred label
     */
    KEYWORDPREFERREDLABEL("//*[self::Anchor or self::CharacterString]"),
    /**
     * 
     */
    KEYWORDURL("//*[self::Anchor]//@href"),
    /**
     * Extract a keyword
     */
    KEYWORD("//*[self::keyword]"),
    /**
     * Extract a keyword group
     */
    KEYWORDGROUP("//*[self::MD_Keywords]"),
    /**
     * Extract a thesaurus name
     */
    THESAURUSNAME("//*[self::thesaurusName]//*[self::CI_Citation]//*[self::title]//*[self::CharacterString or self::Anchor]"),
    /**
     * Extract the URI of a thesaurus
     */
    THESAURUSURI("//*[self::thesaurusName]//*[self::CI_Citation]//*[self::title]//@href"),
    /**
     * Extract the title from an ISO 19139 record
     */
    TITLE ("//*[self::identificationInfo]//*[self::MD_DataIdentification]//*[self::citation]//*[self::CI_Citation]//*[self::title]"),
   /**
    * Extract ISO Digital Transfer options
    */
    DIGITALTRANSFEROPTIONS("//*[self::MD_DigitalTransferOptions]");
    
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
