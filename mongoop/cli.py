# -*- coding: utf-8 -*-
"""
    mongoop.cli
    ~~~~~~~~~~~

    A simple command line application to run mongoop.

    :copyright: (c) 2015 by Lujeni.
    :license: BSD, see LICENSE for more details.
"""

import argparse
import imp
import sys

from mongoop import default_settings as s
from mongoop.core import Mongoop


def main():
    try:
        parser = argparse.ArgumentParser(description=""""Monitor and locate long
            running operations on MongoDB and automatically trigger specific
            actions for alerting and performance analysis.""")
        parser.add_argument('--config', dest='config_file', help='/path/to/settings.py')

        args = parser.parse_args()
        if args.config_file:
            settings = imp.load_source('*', args.config_file)
            s.__dict__.update(settings.__dict__)

        mongoop = Mongoop(
            mongodb_host=s.mongodb_host,
            mongodb_port=s.mongodb_port,
            mongodb_credentials=s.mongodb_credentials,
            mongodb_options=s.mongodb_options,
            frequency=s.frequency,
            triggers=s.triggers,
        )
        mongoop()
    except KeyboardInterrupt:
        sys.exit(0)


if __name__ == '__main__':
    main()
