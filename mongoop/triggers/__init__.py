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


class TriggerSideImplemented(Exception):
    pass


class BaseTrigger(object):
    """ Base to write a trigger.
    """
    def __init__(self, trigger_name, mongoop, operations):
        """ Common stuff for the trigger.

        Args:
            trigger_name (str): the name of the current triger.
            mongoop (object): see mongoo.core
            operations (list): all slow operatations
        """
        self.trigger_name = trigger_name
        self.mongoop = mongoop
        self.params = self.mongoop.triggers[self.trigger_name]

        self._mix_operations = operations
        self.operations = []

    def __call__(self, *args, **kwargs):
        """ Main runner.
        """
        if self.pre_run(*args, **kwargs) and self.operations:
            if self.run(*args, **kwargs):
                self.post_run(*args, **kwargs)

    def pre_run(self):
        """ pre runner.

        BaseTrigger.pre_run create the operations variable.

        Returns:
            bool: True if successful, False otherwise.
        """
        try:
            self.operations = [op for op in self._mix_operations
                               if op['secs_running'] >= self.params['threshold']
                               and op['opid'] not in self.mongoop.opid_by_trigger[self.trigger_name]]
        except Exception as e:
            logging.error('unable to pre_run :: {} :: {}'.format(self.trigger_name, e))
            return False
        else:
            return True

    def post_run(self):
        """ post runner.

        BaseTrigger.post_run update the mongoop.opid_by_trigger variable with
        the opid already process for the current trigger.

        Returns:
            bool: True if successful, False otherwise.
        """
        try:
            [self.mongoop.opid_by_trigger[self.trigger_name].add(operation['opid'])
             for operation in self.operations]
        except Exception as e:
            logging.error('unable to pre_run :: {} :: {}'.format(self.trigger_name, e))
            return False
        else:
            return True

    def run(self):
        """ Must be trigger side implemented.
        """
        raise TriggerSideImplemented
