import pytest
import dataset

import xml.etree.ElementTree


def test_marine_institute_dataset():
    tree = xml.etree.ElementTree.parse("./test/resources/IOOS_Water_Temperature_iso19115.xml")
    ds = dataset.Dataset(tree, dataset.DatasetSourceType.ISO_XML)
    assert ds.title == "Meteorological & Ancillary - Water Temperature"
    assert ds.abstract == "These raw data have not been subjected to the National Ocean Service's quality control or quality assurance procedures and do not meet the criteria and standards of official National Ocean Service data. They are released for limited public use as preliminary data to be used only with appropriate caution."
    assert ds.identifier == "IOOS_Water_Temperature"
