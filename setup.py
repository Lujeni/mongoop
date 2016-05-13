# -*- coding: utf-8 -*-

import os
import sys
from setuptools import find_packages, setup
from setuptools.command.test import test as TestCommand


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


class PyTest(TestCommand):
    user_options = [('pytest-args=', 'a', "Arguments to pass to py.test")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = []

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        #import here, cause outside the eggs aren't loaded
        import pytest
        errno = pytest.main(self.pytest_args)
        sys.exit(errno)


install_requires = [
    'Jinja2==2.8',
    'PyYAML==3.11',
    'pymongo==3.0.2',
]

tests_require = [
    'pytest-cov==2.2.0',
    'pytest-pep8==1.0.6',
    'pytest==2.8.2',
]

setup(
    name='mongoop',
    version='0.6',
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
    install_requires=install_requires,
    tests_require=tests_require,
    cmdclass={'test': PyTest},
    extra_requires={
        'sentry': ['raven==5.5.0'],
        'webhook': ['requests==2.8.1'],
        'graphite': ['graphitesend==0.5.0'],
        'mattermost': ['matterhook==0.1'],
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
