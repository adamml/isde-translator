import unittest
from ie.isde import ISDEDatasetMetadata


class ISDETools(unittest.TestCase):

    _ie_marine_data__dataset_1000 = r"https://irishspatialdataexchange.blob.core.windows.net/metadata/xml/ie_marine_data__dataset_1000.xml"

    def test_dataset_title(self):
        md = ISDEDatasetMetadata().fromISO(self._ie_marine_data__dataset_1000)
        self.assertEqual(md.title == 'CE0613 Site Survey', True)

    def test_dataset_date(self):
        md = ISDEDatasetMetadata().fromISO(self._ie_marine_data__dataset_1000)
        self.assertEqual(md.dateIssued == '2018-11-29', True)


if __name__ == '__main__':
    unittest.main()
