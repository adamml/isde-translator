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

import javax.xml.parsers.ParserConfigurationException;
import javax.xml.xpath.XPathException;
import org.w3c.dom.Document;

/**
 * ThemeCollection extends KeywordCollection to give high level dataset themes 
 * for the dataset. This becomes important for DCAT representations where themes 
 * and keywords are attached to a dcat:Dataset by separate predicates.
 * 
 * @author Adam Leadbetetr
 */
public class ThemeCollection extends KeywordCollection  {

    /**
     *
     * @param doc
     * @throws XPathException
     * @throws ParserConfigurationException
     */
    public ThemeCollection(Document doc) throws javax.xml.xpath.XPathException,
                                 javax.xml.parsers.ParserConfigurationException{
        super(doc);
    }
}
