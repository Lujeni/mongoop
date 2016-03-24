# -*- coding: utf-8 -*-
"""
    mongoop.triggers.mattermost
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~

    :copyright: (c) 2016 by Lujeni.
    :license: BSD, see LICENSE for more details.
"""

import logging

from matterhook import Webhook

from mongoop.triggers import BaseTrigger

logging.basicConfig(
    level=logging.INFO, format='[%(asctime)s] [%(levelname)s] %(message)s')


class MongoopTrigger(BaseTrigger):

    def __init__(self, *args, **kwargs):
        super(MongoopTrigger, self).__init__(*args, **kwargs)

        self.mwh = Webhook(self.params['url'], self.params['api_key'])
        self.mwh.username = self.params.get('username', 'Mongoop')
        self.mwh.icon_url = self.params.get('icon_url', 'https://plugins.qgis.org/static/cache/c8/13/c813bff978535a743f63161bc3a7f937.png')

    def send_hook(self, message):
        try:
            self.mwh.send(message, channel=self.params['channel'])
            logging.info('run :: {} :: {}'.format(self.name))
        except Exception as e:
            logging.error('unable to run :: {} :: {}'.format(self.name, e))
            return False
        else:
            return True

    def op_nok(self, operations):
        for op in operations:
            payload = 'slow operation \n```json\n'
            for key, values in op.items():
                payload += '{}: {}\n'.format(key, values)
            payload += '```'
            self.send_hook(message=payload)

    def op_ok(self):
        return self.send_hook(message='op ok')

    def balancer_nok(self, state):
        return self.send_hook(message='balancer nok :: state={}'.format(state))

    def balancer_ok(self, state):
        return self.send_hook(message='balancer ok :: state={}'.format(state))
