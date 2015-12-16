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

from mongoop.triggers import BaseTrigger


logging.basicConfig(
    level=logging.INFO, format='[%(asctime)s] [%(levelname)s] %(message)s')


class MongoopTrigger(BaseTrigger):

    def __init__(self, *args, **kwargs):
        super(MongoopTrigger, self).__init__(*args, **kwargs)

        database = self.params.get('database', 'mongoop')
        collection = self.params.get('collection', 'history')

        self.db = Database(self.mongoop.conn, database)
        self.collection = self.db.get_collection(collection)
        self.collection.create_index([('opid', DESCENDING)], unique=True, background=True)

    def op_nok(self, operations):
        try:
            if operations:
                self.collection.insert_many(operations)
        except Exception as e:
            logging.error('unable to bulk operations :: {} :: {}'.format(self.name, e))
            return False
        else:
            logging.info('run :: {} :: bulk insert {} operations'.format(self.name, len(operations)))
            return True
