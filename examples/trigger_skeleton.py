# -*- coding: utf-8 -*-
"""
    mongoop.triggers.skeleton
    ~~~~~~~~~~~~~~~~~~~~~~~~~

    Is an example tigger to be used as a template.
    See https://github.com/lujeni/mongoop/wiki/Write-your-own-triggers for more details.

    :copyright: (c) 2015 by Lujeni.
    :license: BSD, see LICENSE for more details.
"""

import logging

from mongoop.triggers import BaseTrigger

logging.basicConfig(
    level=logging.INFO, format='[%(asctime)s] [%(levelname)s] %(message)s')


class MongoopTrigger(BaseTrigger):
    """
    The MongoopTrigger class name is mandatory.
    """

    def __init__(self, *args, **kwargs):
        """
        Necessary to call the parent method (super).

        more details: mongoop.triggers.__init__.BaseTrigger.__call__
        """
        super(MongoopTrigger, self).__init__(*args, **kwargs)

        self.foo = bar

    def op_nok(self, operations):
        """ Main function when a slow operation is found.
        """
        raise NotImplementedError('{} for op_ok'.format(self.type))

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
