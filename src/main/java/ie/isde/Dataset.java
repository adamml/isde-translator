package ie.isde;

import java.io.InputStream;
import java.util.ArrayList;
import java.util.Iterator;
import java.util.List;

import javax.xml.stream.XMLInputFactory;
import javax.xml.stream.XMLStreamReader;
import javax.xml.stream.events.XMLEvent;

import org.apache.jena.query.DatasetFactory;

import org.apache.jena.rdf.model.Model;
import org.apache.jena.rdf.model.ModelFactory;
import org.apache.jena.rdf.model.Resource;

import org.apache.jena.riot.JsonLDWriteContext;
import org.apache.jena.riot.RDFDataMgr;
import org.apache.jena.riot.RDFFormat;
import org.apache.jena.riot.RDFLanguages;
import org.apache.jena.riot.RDFWriter;

import org.apache.jena.riot.system.PrefixMap;
import org.apache.jena.riot.system.RiotLib;

import org.apache.jena.sparql.core.DatasetGraph;

import org.apache.jena.vocabulary.DCAT;
import org.apache.jena.vocabulary.DCTerms;
import org.apache.jena.vocabulary.RDF;
import org.apache.jena.vocabulary.SchemaDO;
import org.apache.jena.vocabulary.SKOS;

/**
* Describes a dataset, that is 	a body of structured data or information
* describing some common topic(s) of interest.
*/
public class Dataset {
	private String abstr;
	private BoundingBox boundingbox;
	private String citation;
	private String doi;
	private String endDate;
	private String identifier;
	private List<String> keywords;
	private String startDate;
	private String source;
	private String title;
	
	
	/**
	* Constructor
	*/
	public Dataset(){}
	/**
	* Cinstructor from an XML InputStreams
	*/
	public Dataset(InputStream xmlstream) throws javax.xml.stream.XMLStreamException { this.from_iso_xml_stream(xmlstream); }
	
	public String abstr(){ return this.abstr; }
	public void abstr(String abstr){ this.abstr = abstr; }
	public BoundingBox boundingbox() { return this.boundingbox; }
	public void boundingbox(BoundingBox bb){ this.boundingbox = bb; }
	public void citation(String cite){ this.citation = cite; }
	public String citation() { return this.citation; }
	public String doi(){ return this.doi; }
	public void doi(String doi){ this.doi = doi; }
	public String endDate() { return this.endDate; }
	public void endDate(String endDate){ this.endDate = endDate; }
	public String identifier() { return this.identifier; }
	public void identifier(String id){ this.identifier = id; }
	public List<String> keywords(){ return this.keywords; }
	public String source() { return this.source; }
	public String startDate() { return this.startDate; }
	public void startDate(String startDate){ this.startDate = startDate; }
	public String title() { return this.title; }
	public void title(String title) { this.title = title; }

	
	private void from_iso_xml_stream(InputStream xmlstream) throws javax.xml.stream.XMLStreamException {
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
					case "dataQualityInfo":
						while (reader.hasNext()) {
							eventType = reader.next();
							if (eventType == XMLEvent.END_ELEMENT) {
								if (reader.getName().getLocalPart() == "dataQualityInfo"){ break; }
							}
						}
						break;
				}
			}
		}
	}
	
	private void parse_iso_xml_stream_md_data_identification(XMLStreamReader reader) throws javax.xml.stream.XMLStreamException {
		int eventType = reader.getEventType();
		while (reader.hasNext()) {
			eventType = reader.next();
			if (eventType == XMLEvent.START_ELEMENT){
				switch (reader.getName().getLocalPart()){
					case "CI_Citation":
						while (reader.hasNext()) {
							eventType = reader.next();
							if (eventType == XMLEvent.START_ELEMENT){
								switch(reader.getName().getLocalPart()){
									case "title":
										this.title(parse_iso_xml_string_return_text_from_gco_characterstring(reader));
										break;
									case "otherCitationDetails":
										this.citation(parse_iso_xml_string_return_text_from_gco_characterstring(reader));
										break;
									case "MD_Identifier":
										while (reader.hasNext()) {
											eventType = reader.next();
											if (eventType == XMLEvent.END_ELEMENT) {
												if (reader.getName().getLocalPart() == "MD_Identifier"){ break;}
											}
										}
										break;
								}
							} else if (eventType == XMLEvent.END_ELEMENT) {
								if (reader.getName().getLocalPart() == "CI_Citation"){break;}
							}
						}
						break;
					case "abstract":
						this.abstr(parse_iso_xml_string_return_text_from_gco_characterstring(reader));
						break;
					case "EX_GeographicBoundingBox":
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
								if (reader.getName().getLocalPart() ==  "EX_GeographicBoundingBox"){
									if(north > -999999 && south > -9999999 && east > -999999 && west > -999999){
										this.boundingbox(new BoundingBox(east, north, south, west));
									}
									break;
								}
							}	
						}
						break;
					case "EX_TemporalExtent":
						while (reader.hasNext()){
							eventType = reader.next();
							if (eventType == XMLEvent.START_ELEMENT){
								switch (reader.getName().getLocalPart()){
									case "beginPosition":
										reader.next();
										try{
											this.startDate(reader.getText());
										} catch (IllegalStateException e){ }
									case "endPosition":
										reader.next();
										try{
											this.endDate(reader.getText());;
										} catch (IllegalStateException e){ }
								}
							}
							else if (eventType == XMLEvent.END_ELEMENT) {
								if (reader.getName().getLocalPart() ==  "EX_TemporalExtent"){ break; }
							}
						}
						break;
					case "MD_AggregateInformation":
						while (reader.hasNext()) {
							eventType = reader.next();
							if (eventType == XMLEvent.END_ELEMENT) {
								if (reader.getName().getLocalPart() == "MD_AggregateInformation"){ break; }
							}
						}
						break;
					case "MD_Keywords":
						while (reader.hasNext()) {
							eventType = reader.next();
							if (eventType == XMLEvent.END_ELEMENT) {
								if (reader.getName().getLocalPart() == "MD_Keywords"){ break; }
							}
						}
						break;
					case "topicCategory":
						while (reader.hasNext()) {
							eventType = reader.next();
							if (eventType == XMLEvent.START_ELEMENT){
								if(reader.getName().getLocalPart() == "MD_TopicCategoryCode"){
									reader.next();
									try{
										this.keywords.add(reader.getText());
									} catch (NullPointerException e){
										this.keywords = new ArrayList<>();
										this.keywords.add(reader.getText());
									}
								}
							} else if (eventType == XMLEvent.END_ELEMENT){
								if(reader.getName().getLocalPart() ==  "topicCategory"){ break; }
							}
						}
						break;
				}
			} else if (eventType == XMLEvent.END_ELEMENT) {
				if (reader.getName().getLocalPart() == "MD_DataIdentification"){ return; }
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
		model.setNsPrefix("adms", "http://www.w3.org/ns/adms#");
		model.setNsPrefix("dcat","http://www.w3.org/ns/dcat#");
		model.setNsPrefix("dct","http://purl.org/dc/terms/");  
		model.setNsPrefix("skos", "http://www.w3.org/2004/02/skos/core#");
		model.setNsPrefix("schema", "https://schema.org/");
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
			dataset.addProperty(DCTerms.identifier, "https://doi.org/" + this.doi());
			Resource doi = model.createResource("https://doi.org/" + this.doi());
			dataset.addProperty(model.createProperty("http://www.w3.org/ns/adms#identifier"), doi);
			doi.addProperty(RDF.type, model.createProperty("http://www.w3.org/ns/adms#Identifier"));
			doi.addProperty(SKOS.notation, "https://doi.org/" + this.doi());
		} catch (NullPointerException e) { }
		try {
			Iterator<String> kwds = this.keywords.iterator();
			while (kwds.hasNext()){
				dataset.addProperty(DCAT.keyword, kwds.next());
			}
		} catch (NullPointerException e) { }
		try {
			String startTime = this.startDate();
			Resource temporal = model.createResource();
			temporal.addProperty(RDF.type, DCTerms.PeriodOfTime);
			temporal.addProperty(SchemaDO.startDate, startTime);
			dataset.addProperty(DCTerms.temporal, temporal);
			temporal.addProperty(SchemaDO.endDate, this.endDate());
		} catch (NullPointerException e){ }
		RDFDataMgr.write(System.out, model, RDFLanguages.TTL);
	}
	
	public void asSchemaDotOrg(){
		Model model = ModelFactory.createDefaultModel();
		model.setNsPrefix("sdo", "https://schema.org/");
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
			doi.addProperty(SchemaDO.name, "DOI: " + this.doi());
			dataset.addProperty(SchemaDO.identifier, doi);
		} catch (NullPointerException e) { }
		try {
			dataset.addProperty(SchemaDO.citation, this.citation());
		} catch (NullPointerException e) { }
		try {
			Iterator<String> kwds = this.keywords.iterator();
			while (kwds.hasNext()){
				dataset.addProperty(SchemaDO.keywords, kwds.next());
			}
		} catch (NullPointerException e) { }
		try{
			String temporal;
			temporal = this.startDate();
			try{
				temporal = temporal + "/" + this.endDate();
			} catch (NullPointerException e){ }
			dataset.addProperty(SchemaDO.temporalCoverage, temporal);
		} catch (NullPointerException e){ }
		DatasetGraph g = DatasetFactory.create(model).asDatasetGraph();
        JsonLDWriteContext ctx = new JsonLDWriteContext();
		String atContextAsJson = "{\"@vocab\":\"https://schema.org/\"}";
        ctx.setJsonLDContext(atContextAsJson);
        RDFWriter w = RDFWriter.create().source(model).format(RDFFormat.JSONLD_COMPACT_PRETTY).context(ctx).base(null).build();
        PrefixMap pm = RiotLib.prefixMap(g);
        w.output(System.out) ;  


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