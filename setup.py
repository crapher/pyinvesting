#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Investing.com API - Market and historical data downloader
# https://github.com/crapher/pyinvesting.git

"""Investing.com API - Market and historical data downloader"""

from setuptools import setup, find_packages
from pyinvesting import __version__
import io
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with io.open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='pyinvesting',
    version=__version__,
    description='Investing.com API - Market and historical data downloader',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/crapher/pyinvesting',
    author='Diego Degese',
    author_email='ddegese@gmail.com',
    license='Apache',
    classifiers=[
        'License :: OSI Approved :: Apache Software License',
        'Development Status :: 3 - Alpha',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'Topic :: Office/Business :: Financial',
        'Topic :: Office/Business :: Financial :: Investment',
        'Topic :: Scientific/Engineering :: Interface Engine/Protocol Translator',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',

        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    platforms=['any'],
    keywords='pandas, investing, online, historical, downloader, finance',
    packages=find_packages(exclude=['contrib', 'docs', 'tests', 'examples']),
    install_requires=['pandas>=1.0.0', 'numpy>=1.18.1', 'requests>=2.21.0', 'websocket-client>=0.57.0', 'pyquery>=1.2']
)
