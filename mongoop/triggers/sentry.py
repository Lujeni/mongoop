# -*- coding: utf-8 -*-
"""
    mongoop.triggers.sentry
    ~~~~~~~~~~~~~~~~~~~~~~~

    :copyright: (c) 2015 by Lujeni.
    :license: BSD, see LICENSE for more details.
"""

import logging

from raven import Client

from mongoop.triggers import BaseTrigger

logging.basicConfig(
    level=logging.INFO, format='[%(asctime)s] [%(levelname)s] %(message)s')


class MongoopTrigger(BaseTrigger):

    def __init__(self, *args, **kwargs):
        super(MongoopTrigger, self).__init__(*args, **kwargs)

        self.client = Client(self.params['dns'])

    def op_nok(self, operations):
        """
        This is the most low-level method available to send a message to sentry.
        """
        try:
            for operation in self.operations:
                result = self.client.captureMessage(
                    message=self.params['message'].format(**operation),
                    data={'level': self.params.get('level', 'info')},
                    extra={'operation': operation}
                )
                logging.info('run :: {} :: {}'.format(self.name, result))
        except Exception as e:
            logging.error('unable to run :: {} :: {}'.format(self.name, e))
            return False
        else:
            return True
