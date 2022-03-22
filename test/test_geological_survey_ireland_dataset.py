import pytest
import isde_dataset

import xml.etree.ElementTree


def test_geological_survey_ireland_dataset():
    tree = xml.etree.ElementTree.parse("./test/resources/d394bf65-a801-4c59-b878-375f631247ed.xml")
    ds = isde_dataset.Dataset(tree, isde_dataset.DatasetSourceType.ISO_XML)
    assert ds.title == "INSS INFOMAR Seabed Samples"
    assert ds.identifier == "d394bf65-a801-4c59-b878-375f631247ed"
    assert ds.bounding_box.north == 57.1
    assert ds.bounding_box.south == 50.01
    assert ds.bounding_box.east == -5.01
    assert ds.bounding_box.west == -17.1
    assert ds.keywords[0] == "oceans"
    assert ds.keywords[1] == "geoscientificInformation"
    assert ds.keywords[2] == "environment"
    assert ds.keywords[3] == "biota"
    with pytest.raises(IndexError):
        ds.keywords[4]
    assert ds.digital_object_identifier == str()
    assert ds.citation_string == str()
