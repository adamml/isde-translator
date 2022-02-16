
[Documentation](https://adamml.github.io/isde-translator/index.html)

## Install
1. Download the repository and unzip it somewhere
1. In a terminal, navigate to the unzipped repository archive
1. Run `python setup.py install` or `pip install -e .`

## Example usage

```console
python translate.py http://data.marine.ie/geonetwork/srv/api/records/ie.marine.data:dataset.1827/formatters/xml -d 
```

```python
import isdetranslator
import urllib.request

with urllib.request.urlopen('http://isde.ie/geonetwork/srv/api/records/ie.nbdc.dataset.RareMarineFishes1786to2008/formatters/xml') as xmldata:
	xmlstr = xmldata.read().decode('utf-8')

ds = isdetranslator.Dataset()
ds.fromXML(xmlstr)

```