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

    def __init__(...):
        """
        NO NEED TO IMPLEMENTED in your trigger

        more details: mongoop.triggers.__init__.BaseTrigger.__call__
        """
        pass

    def __call__(...):
        """
        NO NEED TO IMPLEMENTED in your trigger

        more details: mongoop.triggers.__init__.BaseTrigger.__call__
        """
        pass

    def pre_run(self, *args, **kwargs):
        """
        OPTIONAL TO IMPLEMENTED
        IF IMPLEMENTED:
            - necessary to call the parent method (super)
            - returns True to continue the process (run, post_run)

        more details: mongoop.triggers.__init__.BaseTrigger.pre_run
        """
        try:
            super(MongoopTrigger, self).run(*args, **kwargs)

            print "pre_run task"
        except Exception as e:
            logging.error('unable to pre_run :: {} :: {}'.format(self.trigger_name, e))
            return False
        else:
            return True

    def run(self):
        """ Main function, do what you want.
            Returns True to continue the process (post_run)
        """
        try:
            print "main task"
        except Exception as e:
            logging.error('unable to run :: {} :: {}'.format(self.trigger_name, e))
            return False
        else:
            return True

    def post_run(self, *args, **kwargs):
        """
        OPTIONAL TO IMPLEMENTED
        IF IMPLEMENTED:
            - necessary to call the parent method (super)

        more details: mongoop.triggers.__init__.BaseTrigger.post_run
        """
        try:
            super(MongoopTrigger, self).run(*args, **kwargs)

            print "i am a skeleton post_run"
        except Exception as e:
            logging.error('unable to post_run :: {} :: {}'.format(self.trigger_name, e))
            return False
        else:
            return True
