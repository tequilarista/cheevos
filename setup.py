__author__ = 'tara.hernandez'
import os
from setuptools import setup
from setuptools import setup, find_packages

#
# Only used this for my local pypi server, I don't currently push this to the public pypi
#
 
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()
 
 
setup(
    name = "cheevos",
    version = "0.0.7",
    author = "Tara Hernandez",
    author_email = "tequilarista@gmail.com",
    scripts = ['bin/cheevos'],
    description = ("goofy things to do with project data"),
    license = "BSD",
    keywords = "workflow",
    url = "http://pypi.mycompany.com:8080/simple",
    install_requires = ['jira'],
    packages = find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
    package_data={
        '': [
            "README.md",
            ],
        },
    # TODO: make it work later
    # long_description=read('README.md')
)
