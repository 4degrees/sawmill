# :coding: utf-8
# :copyright: Copyright (c) 2013 Martin Pengelly-Phillips
# :license: See LICENSE.txt.

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


setup(
    name='Mill',
    version='1.0.0dev',
    description='Alternative logging framework for Python',
    packages=[
        'mill',
        'mill.configurator',
        'mill.filterer',
        'mill.formatter',
        'mill.handler',
        'mill.logger'
    ],
    package_dir={
        '': 'source'
    },
    author='Martin Pengelly-Phillips',
    author_email='dev@thesociable.net',
    license='Apache License (2.0)',
    long_description=open('README.rst').read(),
    url='http://github.com/thesociable/mill',
    keywords='logging'
)
