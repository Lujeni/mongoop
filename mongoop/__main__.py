#!/usr/bin/env python
# vim: set fileencoding=utf-8

import argparse
import imp
import sys

from mongoop import default_settings as s
from mongoop.core import MongoOP


def main():
    try:
        parser = argparse.ArgumentParser(description='Locate long running operations and trigger an action')
        parser.add_argument('--config', dest='config_file', help='/path/to/settings.py')

        args = parser.parse_args()
        if args.config_file:
            settings = imp.load_source('*', args.config_file)
            s.__dict__.update(settings.__dict__)

        # NOTE: ugly way to send the arguments.
        mongo_op = MongoOP(s.mongodb_host, s.mongodb_port, s.mongodb_credentials,
            s.mongodb_options, s.mongoop_running_timeout, s.mongoop_frequency,
            s.mongoop_killer, s.mongoop_trigger, s.mongoop_trigger_email)
        mongo_op()
    except KeyboardInterrupt:
        sys.exit(0)


if __name__ == '__main__':
    main()
