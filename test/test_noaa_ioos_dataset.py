import pytest
import isde_dataset

import xml.etree.ElementTree


def test_noaa_ioos_dataset():
    tree = xml.etree.ElementTree.parse("./test/resources/IOOS_Water_Temperature_iso19115.xml")
    ds = isde_dataset.Dataset(tree, isde_dataset.DatasetSourceType.ISO_XML)
    assert ds.title == "Meteorological & Ancillary - Water Temperature"
    assert ds.abstract == "These raw data have not been subjected to the National Ocean Service's quality control or quality assurance procedures and do not meet the criteria and standards of official National Ocean Service data. They are released for limited public use as preliminary data to be used only with appropriate caution."
    assert ds.identifier == "IOOS_Water_Temperature"
    assert ds.bounding_box.north == float()
    assert ds.bounding_box.south == float()
    assert ds.bounding_box.east == float()
    assert ds.bounding_box.west == float()
    assert ds.keywords[0] == "geoscientificInformation"
    with pytest.raises(IndexError):
        ds.keywords[1]
    assert ds.digital_object_identifier == str()
    assert ds.citation_string == str()
