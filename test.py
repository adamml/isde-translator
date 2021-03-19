import unittest
from ie.isde import ISDEDatasetMetadata, RDFNamespaces


class ISDETools(unittest.TestCase):

    _ie_marine_data__dataset_1000 = r"https://irishspatialdataexchange.blob.core.windows.net/metadata/xml/ie_marine_data__dataset_1000.xml"
    _md = ISDEDatasetMetadata().from_iso(_ie_marine_data__dataset_1000)

    def test_dataset_title(self):
        self.assertEqual(self._md.title == 'CE0613 Site Survey', True)

    def test_dataset_date(self):
        self.assertEqual(self._md.dateIssued == '2018-11-29', True)

    def test_dataset_identifier(self):
        self.assertEqual(self._md.identifier == "ie.marine.data:dataset.1000", True)

    def test_rdf_namespaces_dcat_prefix(self):
        self.assertEqual(RDFNamespaces.DCAT['ns'] == 'dcat', True)

    def test_rdf_namespaces_dcat_url(self):
        self.assertEqual(RDFNamespaces.DCAT['url'] == 'http://www.w3.org/ns/dcat#', True)


if __name__ == '__main__':
    unittest.main()
