"""
.. include:: README.md
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
        self._purpose: str = str()
        self._source: str = str()
        self._title: str = str()
        self._start_date: str = str()
        if source_type == DatasetSourceType.ISO_XML:
            self._dataset_from_iso_xml(source)

    @property
    def abstract(self) -> str:
        return self._abstract

    @property
    def bounding_box(self) -> BoundingBox:
        return self._bounding_box

    @property
    def citation_string(self) -> str:
        return self._citation

    @property
    def digital_object_identifier(self) -> str:
        return self._doi

    @property
    def identifier(self) -> str:
        return self._identifier

    @property
    def keywords(self) -> list:
        return self._keywords

    @property
    def title(self) -> str:
        return self._title

    def _dataset_from_iso_xml(self, source: xml.etree.ElementTree.ElementTree):
        try:
            e: List[xml.etree.ElementTree.Element]
            i: xml.etree.ElementTree.Element
            self._title = \
                _str_from_st_and_xpath(source, _XPathQueries.dataset_title)
            _abstract: str = \
                _str_from_st_and_xpath(source, _XPathQueries.dataset_abstract)
            _abstract = _abstract.strip()
            self._abstract = _abstract.replace("\n", " ")
            self._identifier = \
                _str_from_st_and_xpath(source,
                                       _XPathQueries.dataset_file_identifier)
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
            self._bounding_box = BoundingBox(north, south, east, west)
            e = source.findall(_XPathQueries.dataset_themes)
            for i in e:
                self._keywords.append(str(i.text))
            self._doi = \
                _str_from_st_and_xpath(source, _XPathQueries.dataset_uri)
            self._citation = \
                _str_from_st_and_xpath(source, _XPathQueries.dataset_citation)
        except AttributeError:
            pass


def _str_from_st_and_xpath(tree: xml.etree.ElementTree.ElementTree,
                           xpath: str) -> str:
    e: List[xml.etree.ElementTree.Element] = tree.findall(xpath)
    i: xml.etree.ElementTree.Element
    return_string: str = str()
    for i in e:
        return_string = str(i.text)
    return return_string
