"""
A package for working with metadata from the Irish Spatial Data Exchange

## Getting started

1. Download the code repository
    - `git clone https://github.com/adamml/isde-translator.git`
2. Make sure the Python dependencies are properly installed
    - From the root of the cloned repository `python setup.py install`

## Working with dataset metadata records

A major use for this package is working with metadata records which describe datasets. The package can load dataset
metadata records into a native Python object from XML files conforming to the ISO 19139 standard and translate these
native Python objects to Resource Description Framework (RDF) graphs or to plain text following the YAML conventions.

### Loading an Irish Spatial Data Exchange dataset metadata record to Python

#### From an ISO19139 XML record

```python
from ie.isde import ISDEDatasetMetadata

isoRecordURL = r'http://www.isde.ie/geonetwork/srv/api/records/ie.nbdc.dataset.BioMar/formatters/xml'

md = ISDEDatasetMetadata().from_iso(isoRecordURL)
```

### Converting an Irish Spatial Data Exchange dataset metadata record

#### To the W3C's Data Catalog Vocabulary (DCAT)

This conversion is important for connecting to national data infrastructures which, in particular in Europe, may make
use of DCAT application profiles to drive their portals, for example [Ireland's Open Data Portal](https://data.gov.ie).

```python
dcatGraph = md.to_dcat()

# Print the DCAT graph to screen in a Terse Triple Language (TTL) serialisation

dcatGraph.serialize(format='turtle').decode('utf-8')
```

#### To Schema.org

```python
schemaOrgGraph = md.to_schema_org()

# Print the DCAT graph to screen in a JavaScript Object Notation-Linked Data
# (JSON-LD) serialisation

from ie.isde import RDFNamespaces

context = {"@vocab": RDFNamespaces.SDO['url']}

schemaOrgGraph.serialize(format='json-ld', context=context).decode('utf-8')
```

#### To YAML

```python
# Print the `ISDEDatasetMetadata` object to screen as a YAML Ain't Markup
# Language (YAML) document

from yaml import dump, Dumper

dump(md, Dumper=Dumper)
```

## Contributing

Please feel free to contribute to this module by forking it on GitHub and making pull requests against the main
repository.

All class names should begin with an uppercase character.

All method or function names should be entirely lowercase.

All method or function variables should be entirely lowercase.

All methods, functions, classes, attributes and packages should be fully documented with Python docstrings. This module
uses pdoc to generate HTML documentation from Google-style docstrings.

All new contributions should contain unit tests in the `test.py` file.

## License

This module is made available under the Apache 2.0 license.

"""

__docformat__ = "google"

from .ISDEDatasetMetadata import ISDEDatasetMetadata
from .ComplexTypes import ComplexTypes
from .IANAMimeTypes import IANAMimeTypes
from .JSONLDFraming import JSONLDFraming
from .Licenses import Licenses
from .RDFNamespaces import RDFNamespaces


__all__ = ['ISDEDatasetMetadata',
           'ComplexTypes',
           'IANAMimeTypes',
           'JSONLDFraming',
           'Licenses',
           'RDFNamespaces']
