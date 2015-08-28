# -*- coding: utf-8 -*-

import os
from setuptools import find_packages, setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name='mongoop',
    version='0.0.11',
    author='Lujeni',
    author_email='julien@thebault.co',
    description='Monitor and locate long running operations on MongoDB and automatically trigger specific actions for alerting and performance analysis.',
    long_description=read('README.rst'),
    url='https://github.com/lujeni/mongoop',
    download_url='https://github.com/lujeni/mongoop/tags',
    license='BSD',
    platforms='any',
    packages=find_packages(exclude=['tests*']),
    include_package_data=True,
    install_requires=[
        'Jinja2==2.8',
        'PyYAML==3.11',
        'gevent==1.1b3',
        'pymongo==3.0.2',
        'pynsca==1.5',
    ],
    extra_requires={
        'tests': ['pytest'],
        'sentry': ['raven==5.5.0'],
    },
    entry_points={
        'console_scripts': [
            'mongoop = mongoop.cli:main',
        ]
    },
    classifiers=[
        'License :: OSI Approved :: BSD License',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
