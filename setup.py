#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2014 Raphaël Barrois
# This software is distributed under the two-clause BSD license.

import codecs
import os
import re
import sys

from setuptools import setup

root_dir = os.path.abspath(os.path.dirname(__file__))


def get_version(package_name):
    version_re = re.compile(r"^__version__ = [\"']([\w_.-]+)[\"']$")
    package_components = package_name.split('.')
    init_path = os.path.join(root_dir, *(package_components + ['__init__.py']))
    with codecs.open(init_path, 'r', 'utf-8') as f:
        for line in f:
            match = version_re.match(line[:-1])
            if match:
                return match.groups()[0]
    return '0.1.0'


PYPI_PACKAGE = 'django-shareddb'
PACKAGE = 'shareddb'


setup(
    name=PYPI_PACKAGE,
    version=get_version(PACKAGE),
    description="Shared database connections for multi-threaded Django test setups.",
    long_description=''.join(codecs.open('README.rst', 'r', 'utf-8').readlines()),
    author="Raphaël Barrois",
    author_email="raphael.barrois+%s@polytechnique.org" % PACKAGE,
    license="BSD",
    keywords=['django', 'liveserver', 'shared connection'],
    url="https://github.com/rbarrois/%s/" % PYPI_PACKAGE,
    download_url="https://pypi.python.org/pypi/%s/" % PYPI_PACKAGE,
    packages=['shareddb', 'shareddb.backends', 'shareddb.backends.shareddb'],
    install_requires=codecs.open('requirements.txt', 'r', 'utf-8').readlines(),
    setup_requires=[
        'setuptools>=0.8',
    ],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.2",
        "Programming Language :: Python :: 3.3",
    ],
    test_suite='tests',
)
