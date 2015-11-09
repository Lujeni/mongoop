# -*- coding: utf-8 -*-
"""
    mongoop.triggers.webhook
    ~~~~~~~~~~~~~~~~~~~~~~~

    :copyright: (c) 2015 by Lujeni.
    :license: BSD, see LICENSE for more details.
"""

import logging

import requests

from mongoop.triggers import BaseTrigger

logging.basicConfig(
    level=logging.INFO, format='[%(asctime)s] [%(levelname)s] %(message)s')


class MongoopTrigger(BaseTrigger):

    def send_request(self, extra_params):
        try:
            method = getattr(requests, self.params['method'].lower())
            http_params = self.params.get('http_params', {})
            requests_params = self.params.get('requests_params', {})
            http_params['mongoo'] = extra_params
            result = method(self.params['url'], params=http_params, **requests_params)
            if not result.ok:
                raise Exception('{} :: {}'.format(result.status_code, result.reason))
            logging.info('run :: {} :: {}'.format(self.name, result.text))
        except Exception as e:
            logging.error('unable to run :: {} :: {}'.format(self.name, e))
            return False
        else:
            return True


    def op_nok(self, operations):
        """ Send a simple HTTP request.
        """
        return self.send_request(extra_params=[op['opid'] for op in operations])

    def op_ok(self):
        # NOTE: we use the same way to send the HTTP request
        return self.send_request(extra_params=['ok'])

    def balancer_nok(self, state):
        return self.send_request(extra_params=[state])
    
    def balancer_ok(self, state):
        return self.send_request(extra_params=[state])
