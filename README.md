# isde-translator
A tool for translating Irish Spatial Data Exchange metadata

[Documentation](https://adamml.github.io/isde-translator/html/isde/index.html)

## Install
1. Download the repository and unzip it somewhere
2. run `python setup.py install`

## Dependencies
- [rdflib](https://pypi.org/project/rdflib/)
- [rdflib-jsonld](https://pypi.org/project/rdflib-jsonld/)

## Example usage
```python
from ie.isde import ISDEDatasetMetadata, ISDERDFNamespaces

context = {"@vocab": ISDERDFNamespaces.SDO['url']}

print(ISDEDatasetMetadata().fromISO(r'https://irishspatialdataexchange.blob.core.windows.net/metadata/xml/ie_marine_data__dataset_1000.xml').toDCAT().serialize(format='turtle').decode('utf-8'))

print(ISDEDatasetMetadata().fromISO(r'https://irishspatialdataexchange.blob.core.windows.net/metadata/xml/ie_marine_data__dataset_1000.xml').toSchemaOrg().serialize(format='json-ld', context=context).decode('utf-8'))
```
