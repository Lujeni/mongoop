#!/usr/bin/env python
# vim: set fileencoding=utf-8

import logging

from time import sleep

import gevent
from pymongo import MongoClient
from pymongo.database import Database
from pymongo.errors import ConnectionFailure
from pymongo.errors import OperationFailure
from pymongo.read_preferences import ReadPreference

from mongoop.triggers import EmailTrigger
from mongoop.triggers import MongoTrigger

logging.basicConfig(
    level=logging.INFO, format='[%(asctime)s] [%(levelname)s] %(message)s')


class MongoOP(object):

    def __init__(self, mongodb_host, mongodb_port, mongodb_credentials,
                 mongodb_options, mongoop_running_timeout, mongoop_frequency,
                 mongoop_killer, mongoop_trigger, mongoop_trigger_email):
        """
        NOTE: ugly way to manage params
        """
        try:
            # mongodb
            self.mongodb_host = mongodb_host
            self.mongodb_port = mongodb_port
            self.mongodb_credentials = mongodb_credentials or {}
            self.mongodb_options = mongodb_options or {}

            # mongoop
            self.mongoop_running_timeout = mongoop_running_timeout
            self.mongoop_frequency = mongoop_frequency
            self.mongoop_killer = mongoop_killer
            self.kill_in_progress = set()
            self.slow_query = {
                'secs_running': {'$gt': self.mongoop_running_timeout},
                'op': {'$ne': 'none'}
            }

            # mongoop triggers
            self.mongoop_trigger = mongoop_trigger or []
            self.mongoop_trigger_email = mongoop_trigger_email

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
                if self.mongoop_killer:
                    threads.append(gevent.spawn(self._kill_op, op_inprog))

                if 'mongodb' in self.mongoop_trigger:
                    mongoop_trigger_mongodb = MongoTrigger(mongoop=self, operations=op_inprog)
                    threads.append(gevent.spawn(mongoop_trigger_mongodb))

                if 'email' in self.mongoop_trigger:
                    mongoop_trigger_email = EmailTrigger(mongoop=self, operations=op_inprog)
                    threads.append(gevent.spawn(mongoop_trigger_email))

            threads.append(gevent.spawn(sleep, self.mongoop_frequency))
            gevent.joinall(threads)

    def _current_op(self):
        """ Get informations on operations currently running.
        """
        try:
            op_inprog = {}
            coll = self.db.get_collection("$cmd.sys.inprog")
            result = coll.find_one(self.slow_query)
            op_inprog = result.get('inprog', {})
        except Exception as e:
            logging.error('unable to retrieve op :: {}'.format(e))
        else:
            logging.info('find {} slow op'.format(len(op_inprog)))
        finally:
            return op_inprog

    def _kill_op(self, operations):
        """ Terminates an operation as specified by the operation ID.
        :param list operations: List of slow operations.
        """
        try:
            for op in operations:
                opid = op['opid']
                if opid in self.kill_in_progress:
                    raise Exception('kill in progress')
                else:
                    self.kill_in_progress.add(opid)
                self.db.get_collection('$cmd.sys.killop').find_one({'op': opid})
                logging.info('kill op :: {}'.format(opid))
        except Exception as e:
            logging.info('unable to kill op  :: {}'.format(e))
            return False
        else:
            return True
