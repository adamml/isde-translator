package ie.isde;

import java.io.InputStream;
import javax.xml.stream.XMLInputFactory;
import javax.xml.stream.XMLStreamReader;
import javax.xml.stream.events.XMLEvent;

import org.apache.jena.rdf.model.ModelFactory;
import org.apache.jena.rdf.model.Model;
import org.apache.jena.rdf.model.Resource;

import org.apache.jena.vocabulary.DCAT;
import org.apache.jena.vocabulary.DCTerms;
import org.apache.jena.vocabulary.RDF;
import org.apache.jena.vocabulary.SchemaDO;

/**
* Describes a dataset, that is 	a body of structured data or information
* describing some common topic(s) of interest.
*/
public class Dataset {
	private String abstr;
	private BoundingBox boundingbox;
	private String doi;
	private String identifier;
	private String source;
	private String title;
	private boolean title_set;
	
	
	/**
	* Constructor
	*/
	public Dataset(){ this.title_set = false;};
	
	public String abstr(){ return this.abstr; }
	public void abstr(String abstr){ this.abstr = abstr; }
	public BoundingBox boundingbox() { return this.boundingbox; }
	public void boundingbox(BoundingBox bb){ this.boundingbox = bb; }
	public String doi(){ return this.doi; }
	public void doi(String doi){ this.doi = doi; }
	public String identifier() { return this.identifier; }
	public void identifier(String id){ this.identifier = id; }
	public String source() { return this.source; }
	public String title() { return this.title; }
	public void title(String title) { this.title = title; }

	
	public void from_iso_xml_stream(InputStream xmlstream) throws javax.xml.stream.XMLStreamException {
		XMLInputFactory xif = XMLInputFactory.newInstance();
		xif.setProperty(XMLInputFactory.IS_COALESCING, true);
		XMLStreamReader reader = xif.createXMLStreamReader(xmlstream);
		
		int eventType = reader.getEventType();
		while (reader.hasNext()) {
			eventType = reader.next();
			if (eventType == XMLEvent.START_ELEMENT){
				switch (reader.getName().getLocalPart()) {
					case "MD_DataIdentification":
						parse_iso_xml_stream_md_data_identification(reader);
						break;
					case "fileIdentifier":
						this.identifier(parse_iso_xml_string_return_text_from_gco_characterstring(reader));
						break;
					case "dataSetURI":
						this.doi(parse_iso_xml_string_return_text_from_gco_characterstring(reader));
						break;
				}
			}
		}
	}
	
	private void parse_iso_xml_stream_md_data_identification(XMLStreamReader reader) throws javax.xml.stream.XMLStreamException {
		int eventType = reader.getEventType();
		String localPart;
		while (reader.hasNext()) {
			eventType = reader.next();
			if (eventType == XMLEvent.START_ELEMENT){
				switch (reader.getName().getLocalPart()){
					case "CI_Citation":
						parse_iso_xml_stream_ci_citation(reader);
						break;
					case "abstract":
						this.abstr(parse_iso_xml_string_return_text_from_gco_characterstring(reader));
						break;
					case "EX_GeographicBoundingBox":
						parse_iso_xml_stream_ex_geographic_bounding_box(reader);
						break;
				}
			} else if (eventType == XMLEvent.END_ELEMENT) {
				switch (reader.getName().getLocalPart()){
					case "MD_DataIdentification":
						return;
				}
			}
				
		}
		return;
	}
	
	private void parse_iso_xml_stream_ci_citation(XMLStreamReader reader)  throws javax.xml.stream.XMLStreamException {
		int eventType = reader.getEventType();
		
		while (reader.hasNext()) {
			eventType = reader.next();
			if (eventType == XMLEvent.START_ELEMENT){
				switch(reader.getName().getLocalPart()){
					case "title":
						if(this.title_set == false) {
							this.title(parse_iso_xml_string_return_text_from_gco_characterstring(reader));
							this.title_set = true;
						}
				}
			} else if (eventType == XMLEvent.END_ELEMENT) {
				switch (reader.getName().getLocalPart()){
					case "CI_Citation":
						return;
				}
			}
				
		}
		return;
	}
	
	private String parse_iso_xml_string_return_text_from_gco_characterstring(XMLStreamReader reader) throws javax.xml.stream.XMLStreamException {
		int eventType = reader.getEventType();
		while (reader.hasNext()) {
			eventType = reader.next();
			if (eventType == XMLEvent.START_ELEMENT){
				switch(reader.getName().getLocalPart()){
					case "CharacterString":
						reader.next();
						return reader.getText();
				}
			}
		}
		return "";
	}
	
	public void asDCAT(){
		Model model = ModelFactory.createDefaultModel();
		Resource dataset;
		try {
			dataset = model.createResource(this.source);
		} catch (NullPointerException e) {
			dataset = model.createResource();
		}
		dataset.addProperty(RDF.type, DCAT.Dataset);
		try {
			dataset.addProperty(DCTerms.title, this.title());
		} catch (NullPointerException e) { }
		try {
			dataset.addProperty(DCTerms.description, this.abstr());
		} catch (NullPointerException e) { }
		try {
			dataset.addProperty(DCTerms.identifier, this.identifier());
		} catch (NullPointerException e) { }
		try {
			dataset.addProperty(DCTerms.identifier, this.doi());
		} catch (NullPointerException e) { }
		model.write(System.out, "TURTLE");
	}
	
	public void asSchemaDotOrg(){
		Model model = ModelFactory.createDefaultModel();
		Resource dataset;
		try {
			dataset = model.createResource(this.source());
		} catch (NullPointerException e) {
			dataset = model.createResource();
		}
		dataset.addProperty(RDF.type, SchemaDO.Dataset);
		try {
			dataset.addProperty(SchemaDO.name, this.title());
		} catch (NullPointerException e) { }
		try {
			dataset.addProperty(SchemaDO.description, this.abstr());
		} catch (NullPointerException e) { }
		try {
			dataset.addProperty(SchemaDO.identifier, this.identifier());
		} catch (NullPointerException e) { }
		try {
			Resource doi = model.createResource("https://doi.org/" + this.doi());
			doi.addProperty(RDF.type, SchemaDO.PropertyValue);
			doi.addProperty(SchemaDO.propertyID, "https://registry.identifiers.org/registry/doi");
			doi.addProperty(SchemaDO.value, "doi:" + this.doi());
			doi.addProperty(SchemaDO.url, "https://doi.org/" + this.doi());
			dataset.addProperty(SchemaDO.identifier, doi);
		} catch (NullPointerException e) { }
		model.write(System.out, "JSONLD");
	}
	
	private void parse_iso_xml_stream_ex_geographic_bounding_box(XMLStreamReader reader) throws javax.xml.stream.XMLStreamException {
		int eventType = reader.getEventType();
		
		double north = -999999;
		double south = -999999;
		double west = -999999;
		double east = -999999;
		
		while (reader.hasNext()) {
			eventType = reader.next();
			if (eventType == XMLEvent.START_ELEMENT){
				switch(reader.getName().getLocalPart()){
				 	case "northBoundLatitude":
						north = parse_iso_xml_string_return_double_from_gco_decimal(reader);
						break;
					case "southBoundLatitude":
						south = parse_iso_xml_string_return_double_from_gco_decimal(reader);
						break;
					case "eastBoundLongitude":
						east = parse_iso_xml_string_return_double_from_gco_decimal(reader);
						break;
					case "westBoundLongitude":
						west = parse_iso_xml_string_return_double_from_gco_decimal(reader);
						break;
				}
			} else if (eventType == XMLEvent.END_ELEMENT) {
				switch (reader.getName().getLocalPart()){
					case "EX_GeographicBoundingBox":
						if(north > -999999 && south > -9999999 && east > -999999 && west > -999999){
							this.boundingbox(new BoundingBox(east, north, south, west));
						}
						return;
				}
			}
				
		}
		return;
	}
	
	private double parse_iso_xml_string_return_double_from_gco_decimal(XMLStreamReader reader) throws javax.xml.stream.XMLStreamException {
		int eventType = reader.getEventType();
		while (reader.hasNext()) {
			eventType = reader.next();
			if (eventType == XMLEvent.START_ELEMENT){
				switch(reader.getName().getLocalPart()){
					case "Decimal":
						reader.next();
						return Double.valueOf(reader.getText());
				}
			}
		}
		return -999999;
	}
}