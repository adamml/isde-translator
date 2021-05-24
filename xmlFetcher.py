import ie.isde
import os
import urllib.request
from urllib.error import HTTPError
import xml.etree.ElementTree as ET

from pyld import jsonld
from yaml import dump, Dumper

out_dir = ''

with urllib.request.urlopen('http://data.marine.ie/geonetwork/srv/eng/portal.sitemap') as sitemap:
    et = ET.fromstring(sitemap.read())
    for loc in et.findall('.//{http://www.sitemaps.org/schemas/sitemap/0.9}loc'):
        try:
            with urllib.request.urlopen(loc.text.replace('?language=all', '/formatters/xml')) as record:
                framing = ie.isde.JSONLDFraming.DATASET_SCHEMA_ORG.value
                raw_xml = record.read().decode('utf-8')

                isde_metadata = ie.isde.ISDEDatasetMetadata().from_iso(loc.text.replace('?language=all', '/formatters/xml'))
                framing["@id"] = isde_metadata.base_uri

                f = open(os.path.join(out_dir + '/xml', loc.text.replace('?language=all', '/formatters/xml').split('/')[7].replace('.', '_').replace(':', '__') + '.xml'), 'w')
                f.write(raw_xml)
                f.close()
                f = open(os.path.join(out_dir + '/json-ld', loc.text.replace('?language=all', '/formatters/xml').split('/')[7].replace('.', '_').replace(':', '__') + '.json'), 'w')
                f.write(isde_metadata.to_schema_org().serialize(format='json-ld').decode('utf-8'))
                f.close()
                f = open(os.path.join(out_dir + '/dcat', loc.text.replace('?language=all', '/formatters/xml').split('/')[7].replace('.', '_').replace(':', '__') + '.json'), 'w')
                f.write(isde_metadata.to_dcat().serialize(format='turtle').decode('utf-8'))
                f.close()
                f = open(os.path.join(out_dir + '/yaml', loc.text.replace('?language=all', '/formatters/xml').split('/')[7].replace('.', '_').replace(':', '__') + '.yml'), 'w')
                f.write(dump(isde_metadata, Dumper=Dumper))
                f.close()
        except UnicodeEncodeError:
                print("UnicodeEncodeError: " + loc.text.replace('?language=all', '/formatters/xml'))
        except HTTPError:
                print("HTTPError: " + loc.text.replace('?language=all', '/formatters/xml'))
        except TypeError:
                print("TypeError: " + loc.text.replace('?language=all', '/formatters/xml'))
