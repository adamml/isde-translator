import pytest
import isde_dataset

import xml.etree.ElementTree


def test_npws_ireland_dataset():
    tree = xml.etree.ElementTree.parse("./test/resources/eb4307e3-ec47-4f10-905f-d4489f21a54b.xml")
    ds = isde_dataset.Dataset(tree, isde_dataset.DatasetSourceType.ISO_XML)
    assert ds.title == "Wild Nephin National Park Boundary Map"
    assert ds.abstract == "Wild Nephin National Park is Ireland’s sixth National Park and located on the Western seaboard in northwest Mayo. It comprises of circa 15,000 hectares of Atlantic blanket bog and mountainous terrain, covering a vast uninhabited and unspoilt wilderness dominated by the Nephin Beg mountain range. To the west of the mountains is the Owenduff bog. This is one of the last intact active blanket bog systems in Ireland and Western Europe and is an important scientific and scenic feature of the National Park. Wild Nephin National Park is part of the Natura 2000 Network, which protects rare and important habitats and species under the EU Habitats and Birds Directive.  This boundary map is for illustrative purposes only and shall not be held conclusive as to the boundaries or their extent. Please note the Department of Housing Local Government and Heritage makes no representation or provides any warranty as to the accuracy, completeness or currency of this map. The use of this map, which may be altered or updated at any time without notice, is at the sole risk of the user. https://www.nationalparks.ie/"
    assert ds.identifier == "eb4307e3-ec47-4f10-905f-d4489f21a54b"
    assert ds.bounding_box.north == 55.820224054041
    assert ds.bounding_box.south == 51.205966241541006
    assert ds.bounding_box.east == -5.7508110697222
    assert ds.bounding_box.west == -11.265947788472001
    assert ds.keywords[0] == "environment"
    assert ds.keywords[1] == "location"
    with pytest.raises(IndexError):
        ds.keywords[2]
    assert ds.digital_object_identifier == str()
    assert ds.citation_string == str()
