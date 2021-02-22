/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
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
}
