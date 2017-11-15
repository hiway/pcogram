#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from __future__ import (
    absolute_import,
    print_function
)

import io
import re
from glob import glob
from os.path import (
    basename,
    dirname,
    join,
    splitext
)

from setuptools import find_packages, setup


def read(*names, **kwargs):
    return io.open(
        join(dirname(__file__), *names),
        encoding=kwargs.get('encoding', 'utf8')
    ).read()


setup(
    name='pcogram',
    version='0.1.0',
    license='MIT',
    description='A simpler, kinder social network.',
    author='Harshad Sharma',
    author_email='harshad@sharma.io',
    url='https://github.com/hiway/pcogram',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    py_modules=[splitext(basename(path))[0] for path in glob('src/*.py')],
    include_package_data=True,
    zip_safe=False,
    keywords=[
        'social',
        'social network',
        'emoji',
    ],
    install_requires=[
        'click>=6.7, <7.0',
        'requests>=2.18, <3.0',
    ],
    entry_points={
        'console_scripts': [
            'pcogram = pcogram.cli:cli',
        ]
    },
)
