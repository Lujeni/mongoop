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
from time import time
from time import sleep
from sys import exit

from pymongo import MongoClient
from pymongo.database import Database
from pymongo.errors import ConnectionFailure
from pymongo.errors import OperationFailure
from pymongo.read_preferences import ReadPreference


logging.basicConfig(
    level=logging.INFO, format='[%(asctime)s] [%(levelname)s] %(message)s')


class Mongoop(object):

    def __init__(self, mongodb_host, mongodb_port, mongodb_credentials=None,
                 mongodb_options=None, frequency=0, op_triggers=None,
                 balancer_triggers=None, threshold_timeout=None, query=None):
        try:
            # mongodb
            self._mongodb_host = mongodb_host
            self._mongodb_port = mongodb_port
            self._mongodb_credentials = mongodb_credentials or {}
            self._mongodb_options = mongodb_options or {}

            # mongoop triggers
            self._frequency = frequency or 30
            self.op_triggers = op_triggers or {}
            self.balancer_triggers = balancer_triggers or {}
            self._threshold_timeout = threshold_timeout or 60
            self._query = query or {}

            # NOTE: retrieve the minimum threshold.
            if self.op_triggers:
                self._threshold_timeout = min([v['threshold'] for v in self.op_triggers.values() if 'threshold' in v])
            self._base_op_query = {
                'secs_running': {'$gte': self._threshold_timeout},
                'op': {'$ne': 'none'}
            }
            self._base_op_query.update(self._query)

            self.conn = MongoClient(
                host=self._mongodb_host,
                port=self._mongodb_port,
                read_preference=ReadPreference.PRIMARY,
                **self._mongodb_options
            )
            self.db = Database(self.conn, 'admin')
            if self._mongodb_credentials:
                self.db.authenticate(self._mongodb_credentials['username'],
                    self._mongodb_credentials['password'])

            # NOTE: add the callable for each trigger
            self.cycle_op_triggers = []
            self.cycle_balancer_triggers = []

            for t_name, t_values in self.op_triggers.items():
                _callable = self._get_trigger_callable(t_name, t_values)
                if _callable:
                    self.cycle_op_triggers.append(_callable)

            for t_name, t_values in self.balancer_triggers.items():
                _callable = self._get_trigger_callable(t_name, t_values, category='balancer')
                if _callable:
                    self.cycle_balancer_triggers.append(_callable)

        except TypeError as e:
            logging.error('unable to authenticate to admin database :: {}'.format(e))
            exit(1)
        except OperationFailure as e:
            logging.error('authentication failure :: {}'.format(e))
        except ConnectionFailure as e:
            logging.error('unable to connect to database :: {}'.format(e))
        else:
            logging.info('start mongoop :: {}'.format(self))

    def __str__(self):
        return u'{} :: frequency={} :: slow_query={} :: op_triggers={} :: balancer_triggers={}'.format(
            self.conn, self._frequency, self._base_op_query, len(self.cycle_op_triggers),
            len(self.cycle_balancer_triggers))

    def __call__(self):
        """ Main function.
        """
        while True:
            start = time()
            self.call_op_triggers()
            self.call_balancer_triggers()
            exec_time = time() - start
            if exec_time < self._frequency:
                sleep(self._frequency - exec_time)

    def call_op_triggers(self):
        """ Main function to run the op triggers.
        """
        operations = self._current_op()
        for trigger in self.cycle_op_triggers:
            trigger.run(operations=operations)

    def call_balancer_triggers(self):
        """ Main function to run the balancer triggers.
        """
        if not self.balancer_triggers:
            return True

        balancer_state = self._get_balancer_state()
        for trigger in self.cycle_balancer_triggers:
            trigger.run(balancer_state=balancer_state)

    def _get_trigger_callable(self, trigger_name, trigger_params, category='op'):
        """ Retrieve the corresponding trigger by name and add into the triggers list.

        Args:
        """
        try:
            trigger_module = import_module('mongoop.triggers.{}'.format(trigger_params['type']))
            trigger_class = getattr(trigger_module, 'MongoopTrigger')
            trigger = trigger_class(name=trigger_name, params=trigger_params,
                mongoop=self, category=category)
        except Exception as e:
            logging.error('unable to retrieve the trigger callable :: {}'.format(e))
        else:
            return trigger

    def _current_op(self):
        """ Get informations on operations currently running.
        """
        try:
            op_inprog = {}
            coll = self.db.get_collection("$cmd.sys.inprog")
            result = coll.find_one(self._base_op_query)
            op_inprog = result.get('inprog', {})
        except Exception as e:
            logging.error('unable to retrieve op :: {}'.format(e))
        else:
            if op_inprog:
                logging.info('found {} slow op'.format(len(op_inprog)))
            logging.debug('found {} slow op'.format(len(op_inprog)))
        finally:
            return op_inprog

    def _get_balancer_state(self):
        """ Return the balancer state.

            Returns:
                bool: True it's running, False otherwhise.
        """
        try:
            if self.conn.config.settings.find_one({'_id': 'balancer', 'stopped': True}):
                logging.info('balancer state :: stopped')
                return False
            logging.info('balancer state :: started')
            return True
        except Exception as e:
            logging.error('unable to get the balancer state :: {}'.format(e))
