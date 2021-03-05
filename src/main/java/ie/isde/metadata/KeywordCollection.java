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
import com.github.mustachejava.DefaultMustacheFactory;
import com.github.mustachejava.Mustache;
import com.github.mustachejava.MustacheFactory;
import java.io.StringWriter;

import java.util.ArrayList;
import java.util.List;
import javax.xml.parsers.DocumentBuilder;
import javax.xml.parsers.DocumentBuilderFactory;

import javax.xml.xpath.XPathConstants;
import javax.xml.xpath.XPath;
import javax.xml.xpath.XPathFactory;

import org.w3c.dom.Document;
import org.w3c.dom.Node;
import org.w3c.dom.NodeList;

/**
 *
 * @author aleadbetter
 */

public class KeywordCollection {
    
    public final String id;
    public final String url;
    public final String title;
    public final List<Keyword> keyword;
/**
 * Create a KeywordCollection object from a org.w3c.dom.Document object 
 * containing a single ISO 19139 MD_KEYWORDS block
 * 
 * @param doc   A DOM document containing one ISO 19139 MD_KEYWORDS block
 * @throws javax.xml.xpath.XPathException 
     * @throws javax.xml.parsers.ParserConfigurationException 
 */   
    public KeywordCollection(Document doc) 
                                    throws javax.xml.xpath.XPathException,
                                           javax.xml.parsers.ParserConfigurationException {  
        this.keyword = new ArrayList<>();
        XPath xPath = XPathFactory.newInstance().newXPath();
/*
  Get the thesaurus name
*/        
        NodeList nodeList = (NodeList) xPath.compile(IsoXmlQueries.THESAURUSNAME.xPath()).evaluate(
                                      doc, XPathConstants.NODESET);
        String tTitle = null;
        for (int i = 0; i < nodeList.getLength(); i++) {
            Node currentItem = nodeList.item(i);
            tTitle = currentItem.getTextContent().trim();
        }
        this.title = tTitle;
/*
  Get the thesaurus URI
*/
        nodeList = (NodeList) xPath.compile(IsoXmlQueries.THESAURUSURI.xPath()).evaluate(
                                      doc, XPathConstants.NODESET);
        String tUrl = null;
        for (int i = 0; i < nodeList.getLength(); i++) {
            Node currentItem = nodeList.item(i);
            tUrl = currentItem.getTextContent().trim();
        }
        this.url = tUrl;
/*
  Get the individul keywords
*/
        nodeList = (NodeList) xPath.compile(IsoXmlQueries.KEYWORD.xPath()).evaluate(
                                      doc, XPathConstants.NODESET);
        
        Keyword kw;
        DocumentBuilderFactory dbf = DocumentBuilderFactory.newInstance();
        DocumentBuilder db = dbf.newDocumentBuilder();
        Document d;
        
        for (int i = 0; i < nodeList.getLength(); i++) {
            Node currentItem = nodeList.item(i);
            
            d = db.newDocument();
            Node iN = d.importNode(currentItem,true);
            d.appendChild(iN);
            
            kw = new Keyword(d);
            this.keyword.add(kw);
        }
/*
  Set an id for using in RDF graphs
*/
        this.id = NanoIdUtils.randomNanoId();
    } 
    
    @Override
    public String toString()  {
        MustacheFactory mf = new DefaultMustacheFactory();
        Mustache mustache = mf.compile("toString__KeywordCollection.mustache");
        
        StringWriter sw = new StringWriter();
        
        try {
            mustache.execute(sw, this).flush();
        } catch(java.io.IOException e) {}
        
        return sw.toString();
    }
}
