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
		Dataset ds = new Dataset(this.getClass().getResourceAsStream("/ie_marine_data_dataset_3757.xml"));
	}
	
	@Test
	public void ie_marine_data_iso_title() throws javax.xml.stream.XMLStreamException {
		Dataset ds = new Dataset(this.getClass().getResourceAsStream("/ie_marine_data_dataset_3757.xml"));
		assertEquals("Water quality and meteorological data from the Lough Feeagh Automatic Water Quality Monitoring Station (AWQMS), 2004-2019", ds.title());
	}
	
	@Test
	public void gsi_iso_title() throws javax.xml.stream.XMLStreamException {
		Dataset ds = new Dataset(this.getClass().getResourceAsStream("/d394bf65-a801-4c59-b878-375f631247ed.xml"));
		assertEquals("INSS INFOMAR Seabed Samples", ds.title());
	}
	
	@Test
	public void ioos_iso_title() throws javax.xml.stream.XMLStreamException {
		Dataset ds = new Dataset(this.getClass().getResourceAsStream("/IOOS_Water_Temperature_iso19115.xml"));
		assertEquals("Meteorological & Ancillary - Water Temperature", ds.title());
	}
	
	@Test
	public void ioos_iso_abstract() throws javax.xml.stream.XMLStreamException {
		Dataset ds = new Dataset(this.getClass().getResourceAsStream("/IOOS_Water_Temperature_iso19115.xml"));
		assertEquals("These raw data have not been subjected to the National Ocean Service's quality control or quality assurance procedures and do not meet the criteria and standards of official National Ocean Service data. They are released for limited public use as preliminary data to be used only with appropriate caution.", ds.abstr());
	}
	
	@Test
	public void ie_marine_data_iso_bounding_box_north() throws javax.xml.stream.XMLStreamException {
		Dataset ds = new Dataset(this.getClass().getResourceAsStream("/ie_marine_data_dataset_3757.xml"));
		BoundingBox bb = ds.boundingbox();
		assertEquals(53.945276, bb.north());
	}
	
	@Test
	public void ie_marine_data_iso_bounding_box_south() throws javax.xml.stream.XMLStreamException {
		Dataset ds = new Dataset(this.getClass().getResourceAsStream("/ie_marine_data_dataset_3757.xml"));
		BoundingBox bb = ds.boundingbox();
		assertEquals(53.945276, bb.south());
	}
	
	@Test
	public void ie_marine_data_iso_bounding_box_west() throws javax.xml.stream.XMLStreamException {
		Dataset ds = new Dataset(this.getClass().getResourceAsStream("/ie_marine_data_dataset_3757.xml"));
		BoundingBox bb = ds.boundingbox();
		assertEquals(-9.577527, bb.west());
	}
	
	@Test
	public void ie_marine_data_iso_bounding_box_east() throws javax.xml.stream.XMLStreamException {
		Dataset ds = new Dataset(this.getClass().getResourceAsStream("/ie_marine_data_dataset_3757.xml"));
		BoundingBox bb = ds.boundingbox();
		assertEquals(-9.577527, bb.east());
	}
	
	@Test
	public void gsi_iso_bounding_box_north() throws javax.xml.stream.XMLStreamException {
		Dataset ds = new Dataset(this.getClass().getResourceAsStream("/d394bf65-a801-4c59-b878-375f631247ed.xml"));
		BoundingBox bb = ds.boundingbox();
		assertEquals(57.1, bb.north());
	}
	
	@Test
	public void gsi_iso_bounding_box_south() throws javax.xml.stream.XMLStreamException {
		Dataset ds = new Dataset(this.getClass().getResourceAsStream("/d394bf65-a801-4c59-b878-375f631247ed.xml"));
		BoundingBox bb = ds.boundingbox();
		assertEquals(50.01, bb.south());
	}
	
	@Test
	public void gsi_iso_bounding_box_west() throws javax.xml.stream.XMLStreamException {
		Dataset ds = new Dataset(this.getClass().getResourceAsStream("/d394bf65-a801-4c59-b878-375f631247ed.xml"));
		BoundingBox bb = ds.boundingbox();
		assertEquals(-17.1, bb.west());
	}
	
	@Test
	public void gsi_iso_bounding_box_east() throws javax.xml.stream.XMLStreamException {
		Dataset ds = new Dataset(this.getClass().getResourceAsStream("/d394bf65-a801-4c59-b878-375f631247ed.xml"));
		BoundingBox bb = ds.boundingbox();
		assertEquals(-5.01, bb.east());
	}
	
	@Test
	public void gsi_iso_identifier() throws javax.xml.stream.XMLStreamException {
		Dataset ds = new Dataset(this.getClass().getResourceAsStream("/d394bf65-a801-4c59-b878-375f631247ed.xml"));
		assertEquals("d394bf65-a801-4c59-b878-375f631247ed", ds.identifier());
	}
	
	@Test
	public void ie_marine_data_iso_identifier() throws javax.xml.stream.XMLStreamException {
		Dataset ds = new Dataset(this.getClass().getResourceAsStream("/ie_marine_data_dataset_3757.xml"));
		assertEquals("ie.marine.data:dataset.3757", ds.identifier());
	}
	
	@Test
	public void ioos_iso_identifier() throws javax.xml.stream.XMLStreamException {
		Dataset ds = new Dataset(this.getClass().getResourceAsStream("/IOOS_Water_Temperature_iso19115.xml"));
		assertEquals("IOOS_Water_Temperature", ds.identifier());
	}
	
	@Test
	public void ie_marine_data_iso_doi() throws javax.xml.stream.XMLStreamException {
		Dataset ds = new Dataset(this.getClass().getResourceAsStream("/ie_marine_data_dataset_3757.xml"));
		assertEquals("10.20393/edd58462-ae36-44b2-bf36-0ef06c6e8357", ds.doi());
	}
	
	@Test
	public void ie_marine_data_iso_as_dcat() throws javax.xml.stream.XMLStreamException {
		Dataset ds = new Dataset(this.getClass().getResourceAsStream("/ie_marine_data_dataset_3757.xml"));
		ds.asDCAT();
	}
	
	@Test
	public void ie_marine_data_as_iso_schema_dot_org() throws javax.xml.stream.XMLStreamException {
		Dataset ds = new Dataset(this.getClass().getResourceAsStream("/ie_marine_data_dataset_3757.xml"));
		ds.asSchemaDotOrg();
	}
	
	@Test
	public void ie_marine_data_iso_keywords() throws javax.xml.stream.XMLStreamException {
		Dataset ds = new Dataset(this.getClass().getResourceAsStream("/ie_marine_data_dataset_3757.xml"));
		assertEquals("biota", ds.keywords().get(0));
		assertEquals("climatologyMeteorologyAtmosphere", ds.keywords().get(1));
		assertEquals("location", ds.keywords().get(2));
		assertEquals("oceans", ds.keywords().get(3));
	}
	
	@Test
	public void ioos_iso_keywords() throws javax.xml.stream.XMLStreamException {
		Dataset ds = new Dataset(this.getClass().getResourceAsStream("/IOOS_Water_Temperature_iso19115.xml"));
		assertEquals("geoscientificInformation", ds.keywords().get(0));
	}
	
	@Test
	public void gsi_iso_keywords() throws javax.xml.stream.XMLStreamException {
		Dataset ds = new Dataset(this.getClass().getResourceAsStream("/d394bf65-a801-4c59-b878-375f631247ed.xml"));
		assertEquals("oceans", ds.keywords().get(0));
		assertEquals("geoscientificInformation", ds.keywords().get(1));
		assertEquals("environment", ds.keywords().get(2));
		assertEquals("biota", ds.keywords().get(3));
	}
}