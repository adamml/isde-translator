import pytest
import dataset

import xml.etree.ElementTree


def test_marine_institute_dataset():
    tree = xml.etree.ElementTree.parse("./test/resources/ie_marine_data_dataset_3757.xml")
    ds = dataset.Dataset(tree, dataset.DatasetSourceType.ISO_XML)
    assert ds.title == "Water quality and meteorological data from the Lough Feeagh Automatic Water Quality Monitoring Station (AWQMS), 2004-2019"
    assert ds.identifier == "ie.marine.data:dataset.3757"
    assert ds.bounding_box.north == 53.945276
    assert ds.bounding_box.south == 53.945276
    assert ds.bounding_box.east == -9.577527
    assert ds.bounding_box.west == -9.577527
