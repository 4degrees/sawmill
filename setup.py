# :coding: utf-8
# :copyright: Copyright (c) 2013 Martin Pengelly-Phillips
# :license: See LICENSE.txt.

import os
import re

from setuptools import setup, find_packages

ROOT_PATH = os.path.dirname(os.path.realpath(__file__))
RESOURCE_PATH = os.path.join(ROOT_PATH, 'resource')
SOURCE_PATH = os.path.join(ROOT_PATH, 'source')
README_PATH = os.path.join(ROOT_PATH, 'README.rst')

PACKAGE_NAME = 'sawmill'

# Read version from source.
with open(
    os.path.join(SOURCE_PATH, PACKAGE_NAME, '_version.py')
) as _version_file:
    VERSION = re.match(
        r'.*__version__ = \'(.*?)\'', _version_file.read(), re.DOTALL
    ).group(1)


# Compute dependencies.
SETUP_REQUIRES = [
    'sphinx >= 1.2.2, < 2',
    'sphinx_rtd_theme >= 0.1.6, < 1',
    'lowdown >= 0.1.0, < 2',
    'pytest-runner >= 2.7, < 3'
]
INSTALL_REQUIRES = [
    'html2text >= 2016.4.2, < 2016.5',
    'pystache >= 0.5, < 0.6'
]
TEST_REQUIRES = [
    'pytest >= 2.9, < 3',
    'pytest-mock >= 0.11, < 1',
    'pytest-cov >= 2, < 3',
]

# Readthedocs requires Sphinx extensions to be specified as part of
# install_requires in order to build properly.
if os.environ.get('READTHEDOCS', None) == 'True':
    INSTALL_REQUIRES.extend(SETUP_REQUIRES)


setup(
    name=PACKAGE_NAME,
    version=VERSION,
    description='Alternative logging framework for Python',
    long_description=open(README_PATH).read(),
    keywords='logging',
    url='http://github.com/4degrees/sawmill',
    author='Martin Pengelly-Phillips',
    author_email='martin@4degrees.ltd.uk',
    license='Apache License (2.0)',
    packages=find_packages(SOURCE_PATH),
    package_dir={
        '': 'source'
    },
    include_package_data=True,
    setup_requires=SETUP_REQUIRES,
    install_requires=INSTALL_REQUIRES,
    tests_require=TEST_REQUIRES,
    extras_require={
        'setup': SETUP_REQUIRES,
        'tests': TEST_REQUIRES,
        'dev': SETUP_REQUIRES + TEST_REQUIRES
    },
    zip_safe=False
)
