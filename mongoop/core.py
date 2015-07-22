# -*- coding: utf-8 -*-
"""
    mongoop.core
    ~~~~~~~~~~~~

    The core to run mongoop.

    :copyright: (c) 2015 by Lujeni.
    :license: BSD, see LICENSE for more details.
"""

import logging

from importlib import import_module
from time import sleep

from gevent import joinall
from gevent import spawn

from pymongo import MongoClient
from pymongo.database import Database
from pymongo.errors import ConnectionFailure
from pymongo.errors import OperationFailure
from pymongo.read_preferences import ReadPreference


logging.basicConfig(
    level=logging.INFO, format='[%(asctime)s] [%(levelname)s] %(message)s')


class Mongoop(object):

    def __init__(self, mongodb_host, mongodb_port, mongodb_credentials,
                 mongodb_options, frequency, triggers):
        try:
            # mongodb
            self.mongodb_host = mongodb_host
            self.mongodb_port = mongodb_port
            self.mongodb_credentials = mongodb_credentials or {}
            self.mongodb_options = mongodb_options or {}

            # mongoop triggers
            self.already_process = []
            self.frequency = frequency
            self.triggers = triggers or {}
            if self.triggers:
                self.threshold_timeout = min([v['threshold'] for v in self.triggers.values()])
            else:
                self.threshold_timeout = 60

            self.slow_query = {
                'secs_running': {'$gte': self.threshold_timeout},
                'op': {'$ne': 'none'},
                'opid': {'$nin': self.already_process}
            }

            self.conn = MongoClient(
                host=self.mongodb_host,
                port=self.mongodb_port,
                read_preference=ReadPreference.PRIMARY,
                serverSelectionTimeoutMS=5000,
                **self.mongodb_options
            )
            self.db = Database(self.conn, 'admin')
            if self.mongodb_credentials:
                self.db.authenticate(**self.mongodb_credentials)
        except TypeError as e:
            logging.error('unable to authenticate to admin database :: {}'.format(e))
        except OperationFailure as e:
            logging.error('authentication failure :: {}'.format(e))
        except ConnectionFailure as e:
            logging.error('unable to connect to database :: {}'.format(e))

    def __call__(self):
        while True:
            threads = []
            op_inprog = self._current_op()

            if op_inprog:
                for trigger_name in self.triggers.keys():
                    trigger_module = import_module('mongoop.triggers.{}'.format(trigger_name))
                    trigger_class = getattr(trigger_module, 'MongoopTrigger')
                    trigger = trigger_class(trigger_name=trigger_name,
                        mongoop=self, operations=op_inprog)
                    threads.append(spawn(trigger))

            threads.append(spawn(sleep, self.frequency))
            joinall(threads)

    def _current_op(self):
        """ Get informations on operations currently running.
        """
        try:
            op_inprog = {}
            coll = self.db.get_collection("$cmd.sys.inprog")
            result = coll.find_one(self.slow_query)
            op_inprog = result.get('inprog', {})
            [self.already_process.append(op) for op in op_inprog]
        except Exception as e:
            logging.error('unable to retrieve op :: {}'.format(e))
        else:
            logging.info('found {} slow op'.format(len(op_inprog)))
        finally:
            return op_inprog
