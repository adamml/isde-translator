![build workflow](https://github.com/adamml/isde-translator/actions/workflows/build.yml/badge.svg)

# isde_dataset

A Python package for translating dataset metadata between a 
number of different representations

## Dataset representations supported

### Reads

- ISO19115/19139 XML

### Serialises

- Schema.org Dataset class as JSON-Linked Data (JSON-LD)
- World Wide Web Consortium (W3C) Data Catalog Vocabulary 
(DCAT) as Terse Triple Language (TTL) 

## Requirements

- Tested on Python 3.7 and later versions
- Only core Python libraries are used in the main code

## Development dependencies

### Testing

Test are run with `pytest`, and on can be automated with `tox`
for specific Python versions.

### Linting

Code linting is checked with `flake8` and type checking with
`mypy`.

### Building documentation

Documentation is built to HTML with `pdoc`.