# -*- coding: utf-8 -*-
"""
    mongoop.core
    ~~~~~~~~~~~~

    The core to run mongoop.

    :copyright: (c) 2015 by Lujeni.
    :license: BSD, see LICENSE for more details.
"""

import logging

from time import sleep

from gevent import joinall
from gevent import spawn

from pymongo import MongoClient
from pymongo.database import Database
from pymongo.errors import ConnectionFailure
from pymongo.errors import OperationFailure
from pymongo.read_preferences import ReadPreference

from mongoop.triggers import KillerTrigger
from mongoop.triggers import EmailTrigger
from mongoop.triggers import MongoTrigger


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
                # TODO: use a loop instead of condition ?
                if 'killer' in self.triggers:
                    killer_trigger = KillerTrigger(mongoop=self, operations=op_inprog)
                    threads.append(spawn(killer_trigger))

                if 'mongodb' in self.triggers:
                    mongodb_trigger = MongoTrigger(mongoop=self, operations=op_inprog)
                    threads.append(spawn(mongodb_trigger))

                if 'email' in self.triggers:
                    email_trigger = EmailTrigger(mongoop=self, operations=op_inprog)
                    threads.append(spawn(email_trigger))

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
