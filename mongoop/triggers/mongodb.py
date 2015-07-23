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

    def run(self, *args, **kwargs):
        try:
            super(MongoopTrigger, self).run(*args, **kwargs)

            self.collection.insert_many(self.operations)
        except Exception:
            # TODO: logging
            return False
        else:
            logging.info('run :: {} :: bulk insert {} operations'.format(self.trigger_name, len(self.operations)))
            return True
