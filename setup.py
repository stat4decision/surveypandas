# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='surveypandas',
    version='0.1.0',
    description='Python tools for survey data',
    long_description=readme,
    author='Emmanuel Jakobowicz',
    author_email='ej@stat4decision.com',
    url='https://github.com/stat4decision/surveypandas',
    license=license,
    packages=find_packages(exclude=('tests', 'docs'))
)