import pytest
import isdetranslator

def test_dummy_dataset_title():
    ds = isdetranslator.Dataset()
    ds.set(isdetranslator.DatasetProperties.TITLE, 'foo')
    assert ds.title() == 'foo'

def test_dummy_dataset_abstract():
    ds = isdetranslator.Dataset()
    ds.set(isdetranslator.DatasetProperties.ABSTRACT, 'foo')
    assert ds.abstract() == 'foo'
