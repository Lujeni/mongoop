# -*- coding: utf-8 -*-
"""
    mongoop.triggers.mongodb
    ~~~~~~~~~~~~~~~~~~~~~~~~

    :copyright: (c) 2015 by Lujeni.
    :license: BSD, see LICENSE for more details.
"""

import logging

from pymongo.database import Database
from pymongo import DESCENDING
from pymongo.errors import DuplicateKeyError

from mongoop.triggers import BaseTrigger


logging.basicConfig(
    level=logging.INFO, format='[%(asctime)s] [%(levelname)s] %(message)s')


class MongoopTrigger(BaseTrigger):

    def __init__(self, *args, **kwargs):
        super(MongoopTrigger, self).__init__(*args, **kwargs)

        database = self.mongoop.triggers['mongodb'].get('database', 'mongoop')
        collection = self.mongoop.triggers['mongodb'].get('collection', 'history')

        self.db = Database(self.mongoop.conn, database)
        self.collection = self.db.get_collection(collection)
        self.collection.create_index([('opid', DESCENDING)], unique=True, background=True)

    def run(self, *args, **kwargs):
        try:
            super(MongoopTrigger, self).run(*args, **kwargs)

            self.collection.insert_many(self.operations)
        except DuplicateKeyError as e:
            logging.debug('op already trigger :: {}'.format(e))
        except Exception as e:
            logging.error('unable to run :: {} :: {}'.format(self.__class__.__name__, e))
            return False
        else:
            return True
