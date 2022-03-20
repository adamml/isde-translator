__docformat__ = "google"


class BoundingBox(object):
    """This class represents a geographic bounding box comprising the
    northernmost, southernmost, westernmost and westernmost extents of a
    geographic feature.

    Note:
        The class makes no distinction as to the coordinate reference system
        in use and therefore does not apply a range check on creation. Also,
        given that some data may be collected near the date line, the class
        makes no assumptions about east / west extent necessarily being greater
        than each other.

    Args:
        north (float): The northernmost extent of the geographic feature
                        represented by the `BoundingBox`
        south(float): The southernmost extent of the geographic feature
                        represented by the `BoundingBox`
        east(float): The easternmost extent of the geographic feature
                        represented by the `BoundingBox`
        west(float): The westernmost extent of the geographic feature
                        represented by the `BoundingBox`

    Raises:
        TypeError if any input variables are not of type float

    """
    def __init__(self, north: float, south: float, east: float, west: float):
        self._north: float
        self._south: float
        self._east: float
        self._west: float

        if not isinstance(north, float):
            raise TypeError
        elif not isinstance(south, float):
            raise TypeError
        elif not isinstance(east, float):
            raise TypeError
        elif not isinstance(west, float):
            raise TypeError

        self._north = north
        self._south = south
        self._east = east
        self._west = west

    def __str__(self):
        return str(vars(self))

    @property
    def north(self) -> float:
        """float: The northernmost extent of the `BoundingBox`"""
        try:
            return self._north
        except AttributeError:
            return float()

    @property
    def south(self) -> float:
        """float: The southernmost extent of the `BoundingBox`"""
        try:
            return self._south
        except AttributeError:
            return float()

    @property
    def east(self) -> float:
        """float: The easternmost extent of the `BoundingBox`"""
        try:
            return self._east
        except AttributeError:
            return float()

    @property
    def west(self) -> float:
        """float: The westernmost extent of the `BoundingBox`"""
        try:
            return self._west
        except AttributeError:
            return float()
