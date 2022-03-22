import pytest
import isde_dataset

import xml.etree.ElementTree


def test_erddap_irish_weather_buoy_dataset():
    tree = xml.etree.ElementTree.parse("./test/resources/IWBNetwork_iso19115.xml")
    ds = isde_dataset.Dataset(tree, isde_dataset.DatasetSourceType.ISO_XML)
    assert ds.title == "Irish Weather Buoy Network Real Time Data"
    assert ds.abstract == "Real time meteorological and oceanographic data collected from the Irish moored Weather Buoy network  of stations. Parameters collected include: DateTime (yyyy-mm-ddThh:mm:ss.sss), Atmospheric Pressure (mbar), Air Temperature  (degreeCelsius), DewPoint Temperature (degreeCelsius), Wind Speed (knots), Max Gust Wind Speed (knots), Wind Direction (degreeTrue), Sea  Surface Temperature (degreeCelsius), Wave Period (seconds), Wave Height (metres) and Relative Humidity (%). Real time data available for  M2, M3, M4, M5 and M6. Historical data available for M1, FS1 and original M4 spatial location. The network is managed by the Marine  Institute in collaboration with Met Eireann and the UK Met Office. The Irish Weather Buoy Network is designed to improve weather forecasts  and safety at sea around Ireland. The buoy network provides vital data for weather forecasts, shipping bulletins, gale and swell warnings  as well as data for general public information and research."
    assert ds.identifier == "IWBNetwork"
    assert ds.bounding_box.north == 54.999966
    assert ds.bounding_box.south == 51.215958
    assert ds.bounding_box.east == -5.4302
    assert ds.bounding_box.west == -15.88135
    assert ds.keywords[0] == "geoscientificInformation"
    with pytest.raises(IndexError):
        ds.keywords[1]
    assert ds.digital_object_identifier == str()
    assert ds.citation_string == str()
