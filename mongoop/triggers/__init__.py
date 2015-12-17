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

    def __init__(self, name, params, mongoop, category='op'):
        """ Common Stuff for the trigger.

        Args:
            name (str): the name of the trigger.
            params (dict): the necessary trigger params.
            mongoop (object): the mongoop object, usefull to re-use the mongodb connection.
            category (str) (default: op): the category of trigger (op, balancer).
        """
        self.name = name
        self.mongoop = mongoop
        self.category = category
        _params = params

        self.type = _params['type']
        self.threshold = _params.get('threshold', None)
        self.state = _params.get('state', True)
        self.params = _params.get('params', {})
        self.trigger_history = []

    def run(self, operations=None, balancer_state=False):
        """ Init basic and check mandatory stuff before trigger the action.

        Args:
            operations (list): the slow operation.
            balancer_state (bool): the state of the balancer.
        """
        if self.category == 'op':
            self.run_op(operations=operations)
        elif self.category == 'balancer':
            self.run_balancer(balancer_state=balancer_state)

    def run_op(self, operations):
        """ Trigger actions of slow operation type.
        """
        operations = operations or []
        if not self.state and not operations:
            self.op_ok()
        else:
            _operations = []
            for op in operations:
                unique_op = '{opid}_{connectionId}'.format(**op)
                if op['secs_running'] >= self.threshold:
                    if unique_op not in self.trigger_history:
                        _operations.append(op)
                        self.trigger_history.append(unique_op)
                    else:
                        logging.info('{} already process'.format(unique_op))

            if _operations:
                self.op_nok(operations=_operations)

    def run_balancer(self, balancer_state):
        """ Trigger actions of balancer type.

        Args:
            balancer_state (bool): the state of the balancer.
        """
        if balancer_state and self.state:
            self.balancer_ok(state=balancer_state)
        elif not balancer_state and not self.state:
            self.balancer_nok(state=balancer_state)

    def op_nok(self, operations):
        """ Run task when slow operation is found.

        Args:
            operations (list): the slow operation.
        """
        raise NotImplementedError('{} for op_nok'.format(self.type))

    def op_ok(self):
        """ Run task when no slow operation found.
        """
        raise NotImplementedError('{} for op_ok'.format(self.type))

    def balancer_nok(self, state):
        """ Run task when the balancer state is wrong.

        Args:
            state (boolean): True the balancer is running, False otherwhise.
        """
        raise NotImplementedError('{} for balancer_nok'.format(self.type))

    def balancer_ok(self, state):
        """ Run task when the balancer state is good.

        Args:
            state (boolean): True the balancer is running, False otherwhise.
        """
        raise NotImplementedError('{} for balancer_ok'.format(self.type))
