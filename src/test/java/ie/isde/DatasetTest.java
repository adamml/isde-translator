package ie.isde;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;

import java.io.InputStream;

import org.junit.jupiter.api.Test;

public class DatasetTest{
	
	@Test
	public void simple_test_abstr(){
		Dataset ds = new Dataset();
		ds.abstr("foo");
		assertEquals("foo", ds.abstr());
	}
	
	@Test
	public void simple_test_title(){
		Dataset ds = new Dataset();
		ds.title("bar");
		assertEquals("bar", ds.title());
	}
	
	@Test
	public void simple_test_identifier(){
		Dataset ds = new Dataset();
		ds.identifier("baz");
		assertEquals("baz", ds.identifier());
	}
	
	@Test
	public void simple_test_from_iso_stream() throws javax.xml.stream.XMLStreamException {
		Dataset ds = new Dataset();
		ds.from_iso_xml_stream(this.getClass().getResourceAsStream("/ie_marine_data_dataset_3757.xml"));
	}
	
	@Test
	public void ie_marine_data_iso_title() throws javax.xml.stream.XMLStreamException {
		Dataset ds = new Dataset();
		ds.from_iso_xml_stream(this.getClass().getResourceAsStream("/ie_marine_data_dataset_3757.xml"));
		assertEquals(ds.title(), "Water quality and meteorological data from the Lough Feeagh Automatic Water Quality Monitoring Station (AWQMS), 2004-2019");
	}
	
	@Test
	public void gsi_iso_title() throws javax.xml.stream.XMLStreamException {
		Dataset ds = new Dataset();
		ds.from_iso_xml_stream(this.getClass().getResourceAsStream("/d394bf65-a801-4c59-b878-375f631247ed.xml"));
		assertEquals(ds.title(), "INSS INFOMAR Seabed Samples");
	}
	
	@Test
	public void ioos_iso_title() throws javax.xml.stream.XMLStreamException {
		Dataset ds = new Dataset();
		ds.from_iso_xml_stream(this.getClass().getResourceAsStream("/IOOS_Water_Temperature_iso19115.xml"));
		assertEquals(ds.title(), "Meteorological & Ancillary - Water Temperature");
	}
	
	@Test
	public void ioos_iso_abstract() throws javax.xml.stream.XMLStreamException {
		Dataset ds = new Dataset();
		ds.from_iso_xml_stream(this.getClass().getResourceAsStream("/IOOS_Water_Temperature_iso19115.xml"));
		assertEquals(ds.abstr(), "These raw data have not been subjected to the National Ocean Service's quality control or quality assurance procedures and do not meet the criteria and standards of official National Ocean Service data. They are released for limited public use as preliminary data to be used only with appropriate caution.");
	}
	
	@Test
	public void ie_marine_data_iso_bounding_box_north() throws javax.xml.stream.XMLStreamException {
		Dataset ds = new Dataset();
		ds.from_iso_xml_stream(this.getClass().getResourceAsStream("/ie_marine_data_dataset_3757.xml"));
		BoundingBox bb = ds.boundingbox();
		assertEquals(bb.north(), 53.945276);
	}
	
	@Test
	public void ie_marine_data_iso_bounding_box_south() throws javax.xml.stream.XMLStreamException {
		Dataset ds = new Dataset();
		ds.from_iso_xml_stream(this.getClass().getResourceAsStream("/ie_marine_data_dataset_3757.xml"));
		BoundingBox bb = ds.boundingbox();
		assertEquals(bb.south(), 53.945276);
	}
	
	@Test
	public void ie_marine_data_iso_bounding_box_west() throws javax.xml.stream.XMLStreamException {
		Dataset ds = new Dataset();
		ds.from_iso_xml_stream(this.getClass().getResourceAsStream("/ie_marine_data_dataset_3757.xml"));
		BoundingBox bb = ds.boundingbox();
		assertEquals(bb.west(), -9.577527);
	}
	
	@Test
	public void ie_marine_data_iso_bounding_box_east() throws javax.xml.stream.XMLStreamException {
		Dataset ds = new Dataset();
		ds.from_iso_xml_stream(this.getClass().getResourceAsStream("/ie_marine_data_dataset_3757.xml"));
		BoundingBox bb = ds.boundingbox();
		assertEquals(bb.east(), -9.577527);
	}
	
	@Test
	public void gsi_iso_bounding_box_north() throws javax.xml.stream.XMLStreamException {
		Dataset ds = new Dataset();
		ds.from_iso_xml_stream(this.getClass().getResourceAsStream("/d394bf65-a801-4c59-b878-375f631247ed.xml"));
		BoundingBox bb = ds.boundingbox();
		assertEquals(bb.north(), 57.1);
	}
	
	@Test
	public void gsi_iso_bounding_box_south() throws javax.xml.stream.XMLStreamException {
		Dataset ds = new Dataset();
		ds.from_iso_xml_stream(this.getClass().getResourceAsStream("/d394bf65-a801-4c59-b878-375f631247ed.xml"));
		BoundingBox bb = ds.boundingbox();
		assertEquals(bb.south(), 50.01);
	}
	
	@Test
	public void gsi_iso_bounding_box_west() throws javax.xml.stream.XMLStreamException {
		Dataset ds = new Dataset();
		ds.from_iso_xml_stream(this.getClass().getResourceAsStream("/d394bf65-a801-4c59-b878-375f631247ed.xml"));
		BoundingBox bb = ds.boundingbox();
		assertEquals(bb.west(), -17.1);
	}
	
	@Test
	public void gsi_iso_bounding_box_east() throws javax.xml.stream.XMLStreamException {
		Dataset ds = new Dataset();
		ds.from_iso_xml_stream(this.getClass().getResourceAsStream("/d394bf65-a801-4c59-b878-375f631247ed.xml"));
		BoundingBox bb = ds.boundingbox();
		assertEquals(bb.east(), -5.01);
	}
	
	@Test
	public void gsi_iso_identifier() throws javax.xml.stream.XMLStreamException {
		Dataset ds = new Dataset();
		ds.from_iso_xml_stream(this.getClass().getResourceAsStream("/d394bf65-a801-4c59-b878-375f631247ed.xml"));
		assertEquals(ds.identifier(), "d394bf65-a801-4c59-b878-375f631247ed");
	}
	
	@Test
	public void ie_marine_data_iso_identifier() throws javax.xml.stream.XMLStreamException {
		Dataset ds = new Dataset();
		ds.from_iso_xml_stream(this.getClass().getResourceAsStream("/ie_marine_data_dataset_3757.xml"));
		assertEquals(ds.identifier(), "ie.marine.data:dataset.3757");
	}
	
	@Test
	public void ioos_iso_identifier() throws javax.xml.stream.XMLStreamException {
		Dataset ds = new Dataset();
		ds.from_iso_xml_stream(this.getClass().getResourceAsStream("/IOOS_Water_Temperature_iso19115.xml"));
		assertEquals(ds.identifier(), "IOOS_Water_Temperature");
	}
	
	@Test
	public void ie_marine_data_doi() throws javax.xml.stream.XMLStreamException {
		Dataset ds = new Dataset();
		ds.from_iso_xml_stream(this.getClass().getResourceAsStream("/ie_marine_data_dataset_3757.xml"));
		assertEquals(ds.doi(), "10.20393/edd58462-ae36-44b2-bf36-0ef06c6e8357");
	}
	
	@Test
	public void ie_marine_data_as_dcat() throws javax.xml.stream.XMLStreamException {
		Dataset ds = new Dataset();
		ds.from_iso_xml_stream(this.getClass().getResourceAsStream("/ie_marine_data_dataset_3757.xml"));
		ds.asDCAT();
	}
	
	@Test
	public void ie_marine_data_as_schema_dot_org() throws javax.xml.stream.XMLStreamException {
		Dataset ds = new Dataset();
		ds.from_iso_xml_stream(this.getClass().getResourceAsStream("/ie_marine_data_dataset_3757.xml"));
		ds.asSchemaDotOrg();
	}
	
}