package ie.isde;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;

import org.junit.jupiter.api.Test;

public class BoundingBoxTest{
	
	@Test
	public void simple_east_test(){
		BoundingBox bb = new BoundingBox((double) 180, (double) 90, (double) -90, (double) -180);
		assertEquals(bb.east(), (double) 180);
	}
	
	@Test
	public void simple_south_test(){
		BoundingBox bb = new BoundingBox(180, 90, -90, -180);
		assertEquals(bb.south(), -90);
	}
	
	@Test
	public void simple_north_test(){
		BoundingBox bb = new BoundingBox(180, 90, -90, -180);
		assertEquals(bb.north(), 90);
	}
	
	@Test
	public void simple_west_test(){
		BoundingBox bb = new BoundingBox(180, 90, -90, -180);
		assertEquals(bb.west(), -180);
	}
	
	@Test
	public void simple_schema_test_box(){
		BoundingBox bb = new BoundingBox(180, 90, -90, -180);
		assertEquals(bb.to_schema_org(),
			"{\"@type\": \"Place\", \"geo\": { \"@type\": \"GeoShape\", \"box\": \"-90.0 -180.0 90.0 180.0\" }}");
	}
	
	@Test
	public void simple_schema_test_point(){
		BoundingBox bb = new BoundingBox(0, 0, 0, 0);
		assertEquals(bb.to_schema_org(),
			"{\"@type\": \"Place\", \"geo\": { \"@type\": \"GeoCoordinates\", \"latitude\": 0.0, \"longitude\": 0.0 }}");
	}
}