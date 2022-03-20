import pytest
from dataset.boundingbox import BoundingBox


def test_bounding_box_basic():
    bb = BoundingBox(float(90), float(-90), float(180), float(-180))
    assert bb.north == 90
    assert bb.south == -90
    assert bb.east == 180
    assert bb.west == -180
    print(bb)


def test_bounding_box_invocation():
    with pytest.raises(TypeError):
        bb = BoundingBox("a", float(-90), float(180), float(-180))
    with pytest.raises(TypeError):
        bb = BoundingBox(float(90), -"b", float(180), float(-180))
    with pytest.raises(TypeError):
        bb = BoundingBox(float(90), float(-90), "c", float(-180))
    with pytest.raises(TypeError):
        bb = BoundingBox(float(90), float(-90), float(180), -180)
