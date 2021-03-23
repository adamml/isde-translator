import unittest

from ie.isde import ComplexTypes, ISDEDatasetMetadata, RDFNamespaces


class ISDETools(unittest.TestCase):

    _ie_marine_data__dataset_1000 = r"https://irishspatialdataexchange.blob.core.windows.net/metadata/xml/ie_marine_data__dataset_1000.xml"
    _ie_nbdc_dataset_BioMar = r"http://www.isde.ie/geonetwork/srv/api/records/ie.nbdc.dataset.BioMar/formatters/xml"
    _md = ISDEDatasetMetadata().from_iso(_ie_marine_data__dataset_1000)
    _md2 = ISDEDatasetMetadata().from_iso(_ie_nbdc_dataset_BioMar)

    def test_from_iso_dataset_title(self):
        self.assertEqual(self._md.title == 'CE0613 Site Survey', True)

    def test_from_iso_dataset_date(self):
        self.assertEqual(self._md.dateIssued == '2018-11-29', True)

    def test_from_iso_dataset_identifier(self):
        self.assertEqual(self._md.identifier == "ie.marine.data:dataset.1000", True)

    def test_from_iso_bounding_box_north(self):
        self.assertEqual(self._md2.boundingBox['north'] == 55.44532946, True)

    def test_from_iso_bounding_box_south(self):
        self.assertEqual(self._md2.boundingBox['south'] == 51.42459778, True)

    def test_from_iso_bounding_box_west(self):
        self.assertEqual(self._md2.boundingBox['west'] == -10.60604422, True)

    def test_from_iso_bounding_box_east(self):
        self.assertEqual(self._md2.boundingBox['east'] == -5.76884641, True)

    def test_from_iso_bounding_box_to_geojson(self):
        self.assertEqual(self._md2.bounding_box_to_geojson() == '{"type": "Polygon", "coordinates": [[[-10.60604422, 51.42459778], [-10.60604422, 55.44532946], [-5.76884641, 55.44532946], [-5.76884641, 51.42459778], [-10.60604422, 51.42459778]]]}', True)

    def test_from_iso_bounding_box_to_wkt(self):
        self.assertEqual(self._md2.bounding_box_to_wkt() == 'POLYGON ((-10.60604422 51.42459778,-10.60604422 55.44532946,-5.76884641 55.44532946,-5.76884641 51.42459778,-5.76884641 55.44532946))', True)

    def test_from_iso_temporal_extent_end(self):
        self.assertEqual(self._md2.temporalExtent['end'] == '1996-12-31T00:00:00', True)

    def test_from_iso_temporal_extent_start(self):
        self.assertEqual(self._md2.temporalExtent['start'] == '1993-01-01T00:00:00', True)


    def test_rdf_namespaces_dcat_prefix(self):
        self.assertEqual(RDFNamespaces.DCAT['ns'] == 'dcat', True)

    def test_rdf_namespaces_dcat_url(self):
        self.assertEqual(RDFNamespaces.DCAT['url'] == 'http://www.w3.org/ns/dcat#', True)

    def test_complex_types_timeperiod(self):
        self.assertEqual(ComplexTypes.TIMEPERIOD.value == dict(start=None, end=None), True)


if __name__ == '__main__':
    unittest.main()
