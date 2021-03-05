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
 * VariableMeasuredCollection extends KeywordCollection to allow differentiation
 * of Keywords which are explicitly linked to descriptions of the variables
 * measured in the dataset. This is particularly of relevance to Schema.org
 * representations where a sdo:variableMeasured is a predicate.
 * 
 * @author Adam Leadbetter
 */
public class VariableMeasuredCollection extends KeywordCollection {

    /**
     *
     * @param doc
     * @throws XPathException
     * @throws ParserConfigurationException
     */
    public VariableMeasuredCollection(Document doc) 
                                        throws javax.xml.xpath.XPathException,
                                 javax.xml.parsers.ParserConfigurationException{
        super(doc);
    }
}
