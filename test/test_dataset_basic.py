import pytest
import isde_dataset

import xml.etree.ElementTree

def test_dataset_basic():
    ds = isde_dataset.Dataset(xml.etree.ElementTree.ElementTree(), isde_dataset.DatasetSourceType.ISO_XML)
    assert ds.title == str()
    assert ds.citation_string == str()

def test_dataset_invocation():
    with pytest.raises(TypeError):
        isde_dataset.Dataset("bar", isde_dataset.DatasetSourceType.ISO_XML)
    with pytest.raises(TypeError):
        isde_dataset.Dataset(xml.etree.ElementTree.ElementTree(), "foo")