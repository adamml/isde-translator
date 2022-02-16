
[Documentation](https://adamml.github.io/isde-translator/html/isde/index.html)

## Install
1. Download the repository and unzip it somewhere
2. run `python setup.py install`

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