"""This module is designed for the translation of spatial isde_dataset metadata
between a number of different serialisations.

#### Motivation

#### Installation

#### Dependencies

#### Example usage

#### Development dependenices

#### Contributing

"""

from .boundingbox import BoundingBox
from ._xpathqueries import _XPathQueries
from enum import Enum
from typing import List

import xml.etree.ElementTree

__docformat__ = "google"


class DatasetSourceType(Enum):
    """
    Enumeration of valid source types for the Dataset class constructor
    """
    ISO_XML = 1
    """ISO 19139 XML file"""


class Dataset(object):
    """
    Args:
        source (object):
        source_type (DatasetSourceType):

    Raises:
        TypeError: If source is not an xml.etree.ElementTree.ElementTree or
                        if source_type is not from DatasetSourceType
    """

    def __init__(self, source: object, source_type: DatasetSourceType):
        if not isinstance(source_type, DatasetSourceType):
            raise TypeError
        if not isinstance(source, xml.etree.ElementTree.ElementTree):
            raise TypeError
        self._abstract: str = str()
        self._bounding_box: BoundingBox = BoundingBox(float(), float(),
                                                      float(), float())
        self._citation: str = str()
        self._doi: str = str()
        self._end_date: str = str()
        self._identifier: str = str()
        self._keywords: list[str] = list(str())
        self._source: str = str()
        self._title: str = str()
        self._start_date: str = str()
        if source_type == DatasetSourceType.ISO_XML:
            self._dataset_from_iso_xml(source)

    @property
    def abstract(self) -> str:
        try:
            return self._abstract
        except AttributeError:
            return str()

    @property
    def bounding_box(self) -> BoundingBox:
        try:
            return self._bounding_box
        except AttributeError:
            return BoundingBox(float(), float(), float(), float())

    @property
    def citation_string(self) -> str:
        try:
            return self._citation
        except AttributeError:
            return str()

    @property
    def digital_object_identifier(self) -> str:
        try:
            return self._doi
        except AttributeError:
            return str()

    @property
    def identifier(self) -> str:
        try:
            return self._identifier
        except AttributeError:
            return str()

    @property
    def keywords(self) -> list:
        try:
            return self._keywords
        except AttributeError:
            return list(str())

    @property
    def title(self) -> str:
        try:
            return self._title
        except AttributeError:
            return str()

    def _dataset_from_iso_xml(self, source: xml.etree.ElementTree.ElementTree):
        e: List[xml.etree.ElementTree.Element] = source.findall(
                                                _XPathQueries.dataset_title)
        i: xml.etree.ElementTree.Element
        for i in e:
            self._title = str(i.text)
        e = source.findall(_XPathQueries.dataset_abstract)
        for i in e:
            _abstract: str = str(i.text)
            _abstract = _abstract.strip()
            self._abstract = _abstract.replace("\n", " ")
        e = source.findall(_XPathQueries.dataset_file_identifier)
        for i in e:
            self._identifier = str(i.text)
        north: float = float()
        south: float = float()
        east: float = float()
        west: float = float()
        e = source.findall(_XPathQueries.dataset_bounding_north)
        for i in e:
            north = float(str(i.text))
        e = source.findall(_XPathQueries.dataset_bounding_south)
        for i in e:
            south = float(str(i.text))
        e = source.findall(_XPathQueries.dataset_bounding_east)
        for i in e:
            east = float(str(i.text))
        e = source.findall(_XPathQueries.dataset_bounding_west)
        for i in e:
            west = float(str(i.text))
        try:
            self._bounding_box = BoundingBox(north, south, east, west)
        except TypeError:
            pass
        e = source.findall(_XPathQueries.dataset_themes)
        for i in e:
            self._keywords.append(str(i.text))
        e = source.findall(_XPathQueries.dataset_uri)
        for i in e:
            self._doi = str(i.text)
