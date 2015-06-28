#!/usr/bin/env python
# vim: set fileencoding=utf-8

import os
from setuptools import find_packages, setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name='mongoOP',
    version='0.0.1',
    author='Lujeni',
    author_email='julien@thebault.co',
    description='',
    long_description=read('README.rst'),
    url='https://github.com/lujeni/mongoOP',
    download_url='https://github.com/lujeni/mongoOP/tags',
    license='BSD',
    platforms='any',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'pymongo==3.0.2',
        'gevent==1.0.2',
    ],
    entry_points={
        'console_scripts': [
            'mongoop = mongoop.__main__:main',
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
