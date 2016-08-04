#!/usr/bin/env python

from setuptools import setup, find_packages

from setuputils import find_version


setup(
    name='astUtils',
    version=find_version('astUtils/__init__.py'),
    description='tools to processing ast',
    author='x r',
    packages=find_packages(),
    py_modules=['setuputils'],
    entry_points={
        'console_scripts': [
            'astConvert = astUtils.script:run_args',
        ],
    }
)
