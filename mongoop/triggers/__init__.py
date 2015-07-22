# -*- coding: utf-8 -*-
"""
    mongoop.triggers
    ~~~~~~~~~~~~~~~~

    Base trigger of mongoop.

    :copyright: (c) 2015 by Lujeni.
    :license: BSD, see LICENSE for more details.
"""

import logging


logging.basicConfig(
    level=logging.INFO, format='[%(asctime)s] [%(levelname)s] %(message)s')


class BaseTrigger(object):

    def __init__(self, trigger_name, mongoop, operations):
        self.trigger_name = trigger_name
        self.mongoop = mongoop
        self.mix_operations = operations
        self.trigger_threshold = self.mongoop.triggers[self.trigger_name].get('threshold')

    def pre_run(self, *args, **kwargs):
        self.operations = [op for op in self.mix_operations if op['secs_running'] >= self.trigger_threshold]

    def post_run(self, *args, **kwargs):
        pass

    def run(self, *args, **kwargs):
        logging.info('run :: {}'.format(self.trigger_name))

    def __call__(self, *args, **kwargs):
        self.pre_run(*args, **kwargs)
        if self.operations:
            self.run(*args, **kwargs)
            self.post_run(*args, **kwargs)
