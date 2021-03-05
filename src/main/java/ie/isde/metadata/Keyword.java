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

import com.aventrix.jnanoid.jnanoid.NanoIdUtils;

import javax.xml.xpath.XPath;
import javax.xml.xpath.XPathConstants;
import javax.xml.xpath.XPathExpressionException;
import javax.xml.xpath.XPathFactory;

import org.w3c.dom.Document;
import org.w3c.dom.Node;
import org.w3c.dom.NodeList;

/**
 *
 * @author Adam Leadbetter
 */
public class Keyword {
    /**
     * A com.aventrix.jnanoid.jnanoid.NanoIdUtils identifier assigned at the
     * time of object instantiation
     */
    public final String id;
    /**
     * The preferred lexical label for the Keyword
     */
    public final String preferredLabel;
    /**
     * A URL to a definition of the Keyword in a controlled vocabulary
     */
    public final String url;
    
    public Keyword(Document doc) throws XPathExpressionException{
        
        XPath xPath = XPathFactory.newInstance().newXPath();
        this.id = NanoIdUtils.randomNanoId();   
/*
  Get the keyword name
*/        
        NodeList nodeList = (NodeList) xPath.compile(IsoXmlQueries.KEYWORDPREFERREDLABEL.xPath()).evaluate(
                                      doc, XPathConstants.NODESET);
        String pL = null;
        for (int i = 0; i < nodeList.getLength(); i++) {
            Node currentItem = nodeList.item(i);
            pL = currentItem.getTextContent().trim();
        }
        this.preferredLabel = pL;
/*
  Get the keyword URL
*/
        nodeList = (NodeList) xPath.compile(IsoXmlQueries.KEYWORDURL.xPath()).evaluate(
                                      doc, XPathConstants.NODESET);
        String thisUrl = null;
        for (int i = 0; i < nodeList.getLength(); i++) {
            Node currentItem = nodeList.item(i);
            thisUrl = currentItem.getTextContent().trim();
        }
        this.url = thisUrl;
    }
}
