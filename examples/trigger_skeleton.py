# -*- coding: utf-8 -*-
"""
    mongoop.triggers.skeleton
    ~~~~~~~~~~~~~~~~~~~~~~~~~

    :copyright: (c) 2015 by Lujeni.
    :license: BSD, see LICENSE for more details.
"""

import logging

from mongoop.triggers import BaseTrigger

logging.basicConfig(
    level=logging.INFO, format='[%(asctime)s] [%(levelname)s] %(message)s')


class MongoopTrigger(BaseTrigger):

    def pre_run(self, *args, **kwargs):
        try:
            super(MongoopTrigger, self).run(*args, **kwargs)

            print "i am a skeleton pre_run"
        except Exception as e:
            logging.error('unable to pre_run :: {} :: {}'.format(self.trigger_name, e))
            return False
        else:
            return True

    def run(self):
        try:
            print "i am a skeleton"
        except Exception as e:
            logging.error('unable to run :: {} :: {}'.format(self.trigger_name, e))
            return False
        else:
            return True

    def post_run(self, *args, **kwargs):
        try:
            super(MongoopTrigger, self).run(*args, **kwargs)

            print "i am a skeleton post_run"
        except Exception as e:
            logging.error('unable to post_run :: {} :: {}'.format(self.trigger_name, e))
            return False
        else:
            return True
