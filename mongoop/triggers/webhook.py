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
from mongoop.triggers import BaseTriggerBalancer

logging.basicConfig(
    level=logging.INFO, format='[%(asctime)s] [%(levelname)s] %(message)s')


class MongoopTrigger(BaseTrigger):
    # TODO: use requests session ?

    def run(self, *args, **kwargs):
        """
        Simple HTTP request.
        """
        try:
            for operation in self.operations:
                method = getattr(requests, self.params['method'].lower())
                result = method(self.params['url'], params=self.params.get('params', {}),
                    **self.params.get('requests_params', {}))
                if not result.ok:
                    raise Exception('{} :: {}'.format(result.status_code, result.reason))
                logging.info('run :: {} :: {}'.format(self.trigger_name, result.text))
        except Exception as e:
            logging.error('unable to run :: {} :: {}'.format(self.trigger_name, e))
            return False
        else:
            return True


class MongoopTriggerBalancer(BaseTriggerBalancer):

    def run(self, *args, **kwargs):
        """
        Simple HTTP request.
        """
        try:
            method = getattr(requests, self.params['method'].lower())
            result = method(self.params['url'], params=self.params.get('params', {}),
                **self.params.get('requests_params', {}))
            if not result.ok:
                raise Exception('{} :: {}'.format(result.status_code, result.reason))
            logging.info('run :: {} :: {}'.format(self.trigger_name, result.text))
        except Exception as e:
            logging.error('unable to run :: {} :: {}'.format(self.trigger_name, e))
            return False
        else:
            return True
