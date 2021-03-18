# isde-translator
A tool for translating Irish Spatial Data Exchange metadata

[Documentation](https://adamml.github.io/isde-translator/html/isde/index.html)

## Install
1. Download the repository and unzip it somewhere
2. run `python setup.py install`

## Dependencies
- [OWSLib](https://pypi.org/project/OWSLib/) - For parsing ISO19139 XML
- [PyYAML](https://pypi.org/project/PyYAML/) - For serialising the ISDE Metadata as YAML
- [rdflib](https://pypi.org/project/rdflib/) - For building DCAT and Schema.org serialisations
- [rdflib-jsonld](https://pypi.org/project/rdflib-jsonld/) - For serialising Schema.org as JSON following the JSON-LD convention

## Example usage

```python
from ie import ISDEDatasetMetadata, ISDERDFNamespaces
from yaml import dump, Dumper

context = {"@vocab": ISDERDFNamespaces.SDO['url']}

print(ISDEDatasetMetadata().from_iso(
    r'https://irishspatialdataexchange.blob.core.windows.net/metadata/xml/ie_marine_data__dataset_1000.xml').to_dcat().serialize(
    format='turtle').decode('utf-8'))

print(ISDEDatasetMetadata().from_iso(
    r'https://irishspatialdataexchange.blob.core.windows.net/metadata/xml/ie_marine_data__dataset_1000.xml').to_schema_org().serialize(
    format='json-ld', context=context).decode('utf-8'))

print(dump(ISDEDatasetMetadata().from_iso(
    r'https://irishspatialdataexchange.blob.core.windows.net/metadata/xml/ie_marine_data__dataset_1000.xml'),
    Dumper=Dumper))
```
