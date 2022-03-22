import pytest
import isde_dataset

import xml.etree.ElementTree


def test_epa_ireland_dataset():
    tree = xml.etree.ElementTree.parse("./test/resources/fb1abe50-b172-44e1-9028-f0357917c1f6.xml")
    ds = isde_dataset.Dataset(tree, isde_dataset.DatasetSourceType.ISO_XML)
    assert ds.title == "INSPIRE E-PRTR Emission Data"
    assert ds.abstract == "E-PRTR data covering reporting for 2007 to 2018 by EU Member States, Iceland, Liechtenstein, Norway, Serbia and Switzerland."
    assert ds.identifier == "fb1abe50-b172-44e1-9028-f0357917c1f6"
    assert ds.bounding_box.north == 55.37999
    assert ds.bounding_box.south == 51.44555
    assert ds.bounding_box.east == -6.01306
    assert ds.bounding_box.west == -10.47472
    assert ds.keywords[0] == "environment"
    with pytest.raises(IndexError):
        ds.keywords[1]
    assert ds.digital_object_identifier == str()
    assert ds.citation_string == str()
