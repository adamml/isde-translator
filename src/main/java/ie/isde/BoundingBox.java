package ie.isde;

/**
* Describes a spatial extent as a combination of its maximum and minimum points
* in latitue and longitude.
*
* @author Adam Leadbetter
*/
public class BoundingBox {
	private double east;
	private double north;
	private double south;
	private double west;
	
	/**
	* Constructor
	*
	* @author Adam Leadbetter
	* @param east The easternmost extent of the BoundingBox.
	* @param north The northernmost extent of the BoundingBox.
	* @param south The southernmost extent of the BoundingBox.
	* @param west The westernmost extent of the Bounding.
	*/
	public BoundingBox ( double east, double north, double south, double west){
		this.east = east;
		this.west = west;
		this.south = south;
		this.north = north;
	}
	
	/**
	* Access the easternmost extent of the BoundingBox instance
	*
	* @return A numeric representation of the longitude of the BoundingBox's 
	*			eastern extent
	*/
	public double east(){ return this.east; }
	
	/**
	* Access the northernmost extent of the BoundingBox instance
	*
	* @return A numeric representation of the latitude of the BoundingBox's
	*			northern extent
	*/
	public double north(){ return this.north; }
	
	/**
	* Access the southernmost extent of the BoundingBox instance
	*
	* @return A numeric representation of the latitude of the BoundingBox's
	*			southern extent
	*/
	public double south(){ return this.south; }
	
	/**
	* Access the westernmost extent of the BoundingBox instance
	*
	* @return A numeric representation of the longitude of the BoundingBox's 
	*			western extent
	*/
	public double west(){ return this.west; }
	
	/**
	* Creates a string of JSON for inclusin in a Schema.orf serialisation of
	* content. If the BoundingBox has non-equal north/south and east/west
	* pairs then a GeoShape box is output, otherwise GeoCoordinates are used
	* to specify the location of a Point.
	*
	* @return A JSON formatted string which represents the relevant 
	*			serialisation of the BoundingBox
	*/
	public String to_schema_org(){
		if(this.north == this.south && this.east == this.west){
			return String.format("{\"@type\": \"Place\", \"geo\": { \"@type\": \"GeoCoordinates\", \"latitude\": %s, \"longitude\": %s }}",
				this.south, this.west);
		} else {
			return String.format("{\"@type\": \"Place\", \"geo\": { \"@type\": \"GeoShape\", \"box\": \"%s %s %s %s\" }}",
				this.south, this.west, this.north, this.east);
		}
	}
}