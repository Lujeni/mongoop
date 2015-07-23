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
        """
        :param str trigger_name: x
        :param object mongoop: see mongoop.core.Mongoop
        :param list operations: all slow operations detected
        """
        self.trigger_name = trigger_name
        self.mongoop = mongoop
        self.params = self.mongoop.triggers[self.trigger_name]

        self._mix_operations = operations

    def pre_run(self, *args, **kwargs):
        # NOTE: default, all operations are send.
        # We want to keep only the operations which need an action.
        self.operations = [op for op in self._mix_operations
                           if op['secs_running'] >= self.params['threshold']
                           and op['opid'] not in self.mongoop.opid_by_trigger[self.trigger_name]]
        return True

    def post_run(self, *args, **kwargs):
        # NOTE: keep a trace of the opid already process for this trigger.
        [self.mongoop.opid_by_trigger[self.trigger_name].add(op['opid'] for op in self.operations)]

    def run(self, *args, **kwargs):
        pass

    def __call__(self, *args, **kwargs):
        if self.pre_run(*args, **kwargs) and self.operations:
            if self.run(*args, **kwargs):
                self.post_run(*args, **kwargs)
