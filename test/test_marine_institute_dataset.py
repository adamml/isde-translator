import pytest
import isde_dataset

import xml.etree.ElementTree


def test_marine_institute_dataset():
    tree = xml.etree.ElementTree.parse("./test/resources/ie_marine_data_dataset_3757.xml")
    ds = isde_dataset.Dataset(tree, isde_dataset.DatasetSourceType.ISO_XML)
    assert ds.title == "Water quality and meteorological data from the Lough Feeagh Automatic Water Quality Monitoring Station (AWQMS), 2004-2019"
    assert ds.abstract == "Lough Feeagh is a deep humic (brown coloured) lake, typical of many lakes in the west of Ireland. This dataset consists of data from the AWQMS (automatic water quality monitoring station) situated in Lough Feeagh, which is run as part of the Marine Institute’s BurrishooleLTER program in the Burrishoole catchment. The AWQMS is permanently moored in 45 meters of water and includes sensors measuring surface water quality, water temperature profiles and meteorological parameters. All data are recorded at a 2-minute resolution. These data are real time (GMT) and raw - they have not yet been through any quality checking procedures. There may be short term data gaps when we are experiencing technical difficulties. Lough Feeagh is a site in the Global Lake Ecological Observatory Network (www.gleon.org). Sensor information is given in the “Feeagh AWQMS sesnsor Metadata.csv” and the \"metadata.csv\" file, along with other pertinent information. The “Feeagh AWQMS Maintenance Comments” log details routine maintenance which the Burrishoole catchment team record. Quality controlled version of these data may be available as they are processed. Check data.marine.ie for updates.  A log of details about  routine maintenance is updated here: https://github.com/IrishMarineInstitute/BurishooleLTER-Public/blob/master/FeeaghAWQMS%20updates/Feeagh%20AWQMS%20Maintenance%20Comments.xlsx  An overview of sensor reliability is updated here:  https://github.com/IrishMarineInstitute/BurishooleLTER-Public/blob/master/FeeaghAWQMS%20updates/Sensor%20performance%20Feeagh%20raft.xlsx  On 14th April 2020 this dataset was update for to include the 2018 and 2019 data. No edits were made to the data which had already been included in the dataset, so the doi for the dataset was maintained."
    assert ds.identifier == "ie.marine.data:dataset.3757"
    assert ds.bounding_box.north == 53.945276
    assert ds.bounding_box.south == 53.945276
    assert ds.bounding_box.east == -9.577527
    assert ds.bounding_box.west == -9.577527
    assert ds.keywords[0] == "biota"
    assert ds.keywords[1] == "climatologyMeteorologyAtmosphere"
    assert ds.keywords[2] == "location"
    assert ds.keywords[3] == "oceans"
    assert ds.digital_object_identifier == "10.20393/edd58462-ae36-44b2-bf36-0ef06c6e8357"
