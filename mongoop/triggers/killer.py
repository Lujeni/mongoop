# -*- coding: utf-8 -*-
"""
    mongoop.triggers.killer
    ~~~~~~~~~~~~~~~~~~~~~~~

    :copyright: (c) 2015 by Lujeni.
    :license: BSD, see LICENSE for more details.
"""

import logging

from mongoop.triggers import BaseTrigger

logging.basicConfig(
    level=logging.INFO, format='[%(asctime)s] [%(levelname)s] %(message)s')


class MongoopTrigger(BaseTrigger):

    def run(self, *args, **kwargs):
        """ Terminates an operation as specified by the operation ID.
        """
        try:
            super(MongoopTrigger, self).run(*args, **kwargs)

            for operation in self.operations:
                opid = operation['opid']
                result = self.mongoop.db.get_collection('$cmd.sys.killop').find_one(
                    {'op': opid})
                logging.info('run :: {} :: {} {}'.format(self.__class__.__name__, result.get('info', 'op'), opid))
        except Exception as e:
            logging.error('unable to run :: {} :: {}'.format(self.__class__.__name__, e))
            return False
        else:
            return True