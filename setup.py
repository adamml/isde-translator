from setuptools import setup

with open("README.md", 'r') as f:
    long_description = f.read()

with open("requirements.txt", 'r') as f:
    requirements = f.read().splitlines() 

setup(
   name='ie.isde',
   version='0.1',
   description='A module of tools for working with metadata from the Irish Spatial Data Exchange',
   license="Apache 2.0",
   long_description=long_description,
   author='Adam Leadbetter',
   url="https://github.com/adamml/isde-translator",
   packages=['ie.isde'],  #same as name
   install_requires=['wheel', 'bar', 'greek']
)