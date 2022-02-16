"""Allows translation of Irish Spatial Data Exchange metadata from ISO 19115/
19139 to other serialisations (W3C DCAT, Schema.org)."""

from enum import Enum

import xml.etree.ElementTree as ET

class BoundingBox:
    """Describes an object containing a geographic bounding box representing the
    spatial extent covered by a dataset"""
    __east = None
    __north = None
    __south = None
    __west = None

    def __init__(self, easternmostLong, northernmostLat, southernmostLat,
                 westernmostLong):
        """Builds an instance of BoundingBox

        Args:
            easternmostLong (float): The easternmost longitude to be represented
                                        by the BoundingBox
            northernmostLat (float): The northernmost latitude to be represented
                                        by the BoundingBox
            southernmostLat (float): The southernmost latitude to be represented
                                        by the BoundingBox
            westernmostLong (float): The westernmost longitude to be represented
                                        by the BoundingBox

        Returns:
            BoundingBox: The constructed instance

        Raises:
            TypeError: If any of the input arguments are not float
        """

        if not isinstance(easternmostLong, float):
            raise TypeError("All inputs to BoundingBox must be of type float")
        if not isinstance(westernmostLong, float):
            raise TypeError("All inputs to BoundingBox must be of type float")
        if not isinstance(northernmostLat, float):
            raise TypeError("All inputs to BoundingBox must be of type float")
        if not isinstance(southernmostLat, float):
            raise TypeError("All inputs to BoundingBox must be of type float")
        
        self.__east = easternmostLong
        self.__north = northernmostLat
        self.__south = southernmostLat
        self.__west = westernmostLong

    def east(self):
        """Gets the easternmost longitude of the BoundingBox instance

        Returns:
            float: The easternmost longitude of the BoundingBox instance
        """
        return self.__east

    def north(self):
        """Gets the northernmost latitude of the BoundingBox instance

        Returns:
            float: The northenmost latitude of the BoundingBox instance
        """
        return self.__north

    def south(self):
        """Gets the southernmost latitude of the BoundingBox instance

        Returns:
            float: The southernmost latitude of the BoundingBox instance
        """
        return self.__south

    def west(self):
        """Gets the westernmost longitude of the BoundingBox instance

        Returns:
            float: The westernmost longitude of the BoundingBox instance
        """
        return self.__west
    

class DataMode(Enum):
    """Enumerates the possible modes of input"""
    FILE = 0
    """Uses a local file for input"""
    WEB = 1
    """Uses a web address for input"""

class Dataset:
    """A class for holding the metadata describing a dataset as described in
    the Irish Spatial Data Exchange."""
    __abstract = None
    __boundingbox = None
    __mode = None
    __source = None
    __title = None

    def __init__(self):
        pass

    def abstract(self):
        """Get the abstract for the Dataset, providing a lexical description of
        the dataset. An abstract should include the who, what, when, where, why
        and how associated with a Dataset.

        Returns:
            str or None: The return value is the abstract for this instance of
                            Dataset
        """
        return self.__abstract

    def fromXML(self, xmlstring):
        """Sets the attributes of Dataset from an XML string which conforms to
        the ISO19115/19139 standard.


        Args:
            xmlstring (str): A Python string representing an XML document
                                formatted to ISO 19115/19139 specifications

        Raises:
            TypeError: If xmlstring is not of type str
        """
        print(type(xmlstring))
        if not isinstance(xmlstring, str):
            raise TypeError("Supplied variable xmlstring must be of type str")
        
        tree = ET.fromstring(xmlstring)

        #
        # Extract the title
        #
        
        for ident in tree.iter("{http://www.isotc211.org/2005/gmd}identificationInfo"):
            for cite in ident.iter("{http://www.isotc211.org/2005/gmd}citation"):
                for title in cite.iter("{http://www.isotc211.org/2005/gmd}title"):
                    for gco in title.iter("{http://www.isotc211.org/2005/gco}CharacterString"):
                        self.set(DatasetProperties.TITLE, gco.text)
        #
        # Extract the abstract
        #
            for abstract in ident.iter("{http://www.isotc211.org/2005/gmd}abstract"):
                for gco in abstract.iter("{http://www.isotc211.org/2005/gco}CharacterString"):
                    self.set(DatasetProperties.ABSTRACT, gco.text)
        #
        # Extract the geographic extent
        #
            for extent in ident.iter("{http://www.isotc211.org/2005/gmd}extent"):
                for bbox in extent.iter("{http://www.isotc211.org/2005/gmd}EX_GeographicBoundingBox"):
                    east = None
                    north = None
                    south = None
                    west = None
                    for westB in bbox.iter("{http://www.isotc211.org/2005/gmd}westBoundLongitude"):
                        for decimal in westB.iter("{http://www.isotc211.org/2005/gco}Decimal"):
                            west = float(decimal.text)
                    for eastB in bbox.iter("{http://www.isotc211.org/2005/gmd}eastBoundLongitude"):
                        for decimal in eastB.iter("{http://www.isotc211.org/2005/gco}Decimal"):
                            east = float(decimal.text)
                    for northB in bbox.iter("{http://www.isotc211.org/2005/gmd}northBoundLatitude"):
                        for decimal in northB.iter("{http://www.isotc211.org/2005/gco}Decimal"):
                            north = float(decimal.text)
                    for southB in bbox.iter("{http://www.isotc211.org/2005/gmd}southBoundLatitude"):
                        for decimal in southB.iter("{http://www.isotc211.org/2005/gco}Decimal"):
                            south = float(decimal.text)
                    if north and south and east and west:
                        self.set(DatasetProperties.BOUNDINGBOX,
                                 BoundingBox(east, north, south, west))
    
    def mode(self):
        """Get the mode for collecting the information for building the Dataset
        instance

        Returns:
            DataMode: A value from DataMode indicating the data source type
        """
        return self.__mode

    def set(self, attr, val):
        """Set properties of a Dataset instance.

        Args:
            attr (DatasetProperties): The property of Dataset to be set
            val: The value to be assigned to the proprty specified in attr
        """
        if attr == DatasetProperties.ABSTRACT:
            self.__abstract = val
        elif attr == DatasetProperties.MODE:
            self.__mode = val
        elif attr == DatasetProperties.SOURCE:
            self.__source = val
        elif attr == DatasetProperties.TITLE:
            self.__title = val
    
    def source(self):
        """Get the data source used to construct the Dataset instance

        Returns:
            str or None: The data source used to construct the Dataset instance
        """
        return self.__source

    def title(self):
        """Get the title, or lexical label, of the Dataset instance

        Returns:
            str or None: The title of the Dataset instance
        """
        return self.__title

class DatasetProperties(Enum):
    """Enumerates the available attributes of a Dataset. Used to constrain the
    inputs to the Dataset.set method"""
    ABSTRACT = 0
    BOUNDINGBOX = 1
    MODE = 2
    SOURCE = 3
    TITLE = 4

class NoInputDataSourceSupplied(Exception):
    """Exception to be raised if no file path or web address is supplied for
    data input"""
    pass

class NoOrIncorrectOutputFormatSupplied(Exception):
    """Exception to be raised on invocation check if there is no output format
    supplied, or if the suplied output format cannot be mapped to a SerialiseAs
    value."""
    pass

class SerialiseAs(Enum):
    """Enumerates the output formats supported by the module."""
    DCAT = 1
    """W3C Data Catalog Vocabulary"""
    SCHEMAORG = 2
    """Schema.org type Datasetss"""
