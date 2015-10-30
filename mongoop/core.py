# -*- coding: utf-8 -*-
"""
    mongoop.core
    ~~~~~~~~~~~~

    The core to run mongoop.

    :copyright: (c) 2015 by Lujeni.
    :license: BSD, see LICENSE for more details.
"""

import logging

from collections import defaultdict
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

    def __init__(self, mongodb_host, mongodb_port, mongodb_credentials=None,
                 mongodb_options=None, frequency=0, triggers=None, threshold_timeout=None, extra_checks=None):
        try:
            # mongodb
            self._mongodb_host = mongodb_host
            self._mongodb_port = mongodb_port
            self._mongodb_credentials = mongodb_credentials or {}
            self._mongodb_options = mongodb_options or {}

            # mongoop triggers
            self._frequency = frequency or 30
            self.opid_by_trigger = defaultdict(set)
            self.triggers = triggers or {}

            self._threshold_timeout = threshold_timeout or 60
            if self.triggers:
                self._threshold_timeout = min([v['threshold'] for v in self.triggers.values()])

            self._slow_query = {
                'secs_running': {'$gte': self._threshold_timeout},
                'op': {'$ne': 'none'},
            }

            # mongoop extra checks
            self.extra_checks = extra_checks or {}

            self.conn = MongoClient(
                host=self._mongodb_host,
                port=self._mongodb_port,
                read_preference=ReadPreference.PRIMARY,
                serverSelectionTimeoutMS=5000,
                **self._mongodb_options
            )
            self.db = Database(self.conn, 'admin')
            if self._mongodb_credentials:
                self.db.authenticate(**self._mongodb_credentials)
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

            # TODO: DRY the mongoop triggers.
            if 'balancer' in self.extra_checks:
                balancer = self.extra_checks['balancer']
                if self._is_balancer_stopped() == balancer['enabled']:
                    for trigger_name in balancer.get('triggers', []):
                        trigger_module = import_module('mongoop.triggers.{}'.format(trigger_name))
                        trigger_class = getattr(trigger_module, 'MongoopTriggerBalancer')
                        trigger = trigger_class(trigger_name=trigger_name,
                                                mongoop=self)
                        threads.append(spawn(trigger))

            threads.append(spawn(sleep, self._frequency))
            joinall(threads)

    def _current_op(self):
        """ Get informations on operations currently running.
        """
        try:
            op_inprog = {}
            coll = self.db.get_collection("$cmd.sys.inprog")
            result = coll.find_one(self._slow_query)
            op_inprog = result.get('inprog', {})
        except Exception as e:
            logging.error('unable to retrieve op :: {}'.format(e))
        else:
            logging.info('found {} slow op'.format(len(op_inprog)))
        finally:
            return op_inprog

    def _is_balancer_stopped(self):
        """ Determine if the balancer is currently enabled or disabled.

            Returns:
                bool: False it's running, True otherwhise.
        """
        try:
            if self.conn.config.settings.find_one({'_id': 'balancer', 'stopped': True}):
                logging.info('balancer state :: stopped')
                return True
            logging.info('balancer state :: started')
            return False
        except Exception as e:
            logging.error('unable to get the balancer state :: {}'.format(e))
