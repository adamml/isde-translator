import pytest
import dataset

import xml.etree.ElementTree


def test_marine_institute_dataset():
    tree = xml.etree.ElementTree.parse("./test/resources/d394bf65-a801-4c59-b878-375f631247ed.xml")
    ds = dataset.Dataset(tree, dataset.DatasetSourceType.ISO_XML)
    assert ds.title == "INSS INFOMAR Seabed Samples"
    assert ds.identifier == "d394bf65-a801-4c59-b878-375f631247ed"
    assert ds.bounding_box.north == 57.1
    assert ds.bounding_box.south == 50.01
    assert ds.bounding_box.east == -5.01
    assert ds.bounding_box.west == -17.1
