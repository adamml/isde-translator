![build workflow](https://github.com/adamml/isde-translator/actions/workflows/build.yml/badge.svg)

# isde_dataset

A Python package for translating dataset metadata between a 
number of different representations

## Motivation

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

## Installation

## Development dependencies

- [flake8](https://pypi.org/project/flake8/) >= 4.0.1
- [mypy](https://pypi.org/project/mypy/) >= 0.941
- [pytest](https://pypi.org/project/pytest/) >= 7.1.1
- [pytest-cov](https://pypi.org/project/pytest-cov/) >= 3.0.0
- [pytest-flake8](https://pypi.org/project/pytest-flake8/) >= 1.1.1
- [pytest-mypy](https://pypi.org/project/pytest-mypy/) > = 0.9.1
- [tox](https://pypi.org/project/tox/) >= 3.24.5

### Testing

Test are run with `pytest`, and on can be automated with `tox`
for specific Python versions. The `tox` tests can be mimicked in 
a local environment with:

````commandline
pytest --cov=isde_dataset --cov-report html --flake8
````

### Linting

Code linting is checked with `flake8` and type checking with
`mypy`.

### Building documentation

Documentation is built to HTML with `pdoc`, e.g.:

````commandline
pdoc src/isde_dataset -o docs
````