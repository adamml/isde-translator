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
 * Represents the metadata object describing a dataset in the  Irish Spatial 
 * Data Exchange
 * 
 * @author Adam Leadbetter
 */
public interface IDataset {
    /**
     * Populates an object's attributes from an ISO XML record
     * 
     * @param isoLocator    String    The file path or URI of an ISO XML 
     *                                metadata record conforming to the Irish
     *                                Spatial Data Infrastructure profile.
     * @throws java.io.IOException
     * @throws javax.xml.parsers.ParserConfigurationException
     * @throws org.xml.sax.SAXException
     * @throws javax.xml.xpath.XPathException
     */
    public void fromISO(String isoLocator)
                throws java.io.IOException,
                       javax.xml.parsers.ParserConfigurationException,
                       org.xml.sax.SAXException,
                       javax.xml.xpath.XPathException;

    /**
     * Get the abstract (describing the who, what, when, where and why) of the
     * dataset
     * 
     * @return The abstract for the dataset
     */
    public String metadataAbstract();
    /**
     * Returns the base URI for the dataset, particularly useful when building
     * Linked Data representations of the dataset's metadata
     * 
     * @return The base URI for the dataset
     */
    public String baseUri();
    /**
     * Returns the title of the dataset represented by the metadata object
     * 
     * @return The title of the dataset
     */
    public String title();
    /**
     * Returns the identifier of the record as a file system safe string for
     * saving the record to disk, minus the file extension
     * 
     * @return A file system safe name for saving the dataset metadata record
     */
    public String identifierToFileName();
    /**
     * Return the file identifier extracted from the metadata record as a String,
     * or null if not initialised.
     * 
     * @return The file identifier as a String
     */
    public String fileIdentifier();
    public String dateIssued();
}
