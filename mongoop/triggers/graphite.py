# -*- coding: utf-8 -*-
"""
    mongoop.triggers.graphite
    ~~~~~~~~~~~~~~~~~~~~~~~~~

    :copyright: (c) 2016 by Lujeni.
    :license: BSD, see LICENSE for more details.
"""

import logging
import os

from collections import Counter

import graphitesend

from mongoop.triggers import BaseTrigger


logging.basicConfig(
    level=logging.INFO, format='[%(asctime)s] [%(levelname)s] %(message)s')

PATH = os.path.dirname(os.path.abspath(__file__))

class MongoopTrigger(BaseTrigger):

    def op_nok(self, operations):
        try:
            counter = Counter([ns['ns'] for ns in operations])
            graphite = graphitesend.init(**self.params.get('graphitesend_params', {}))

            graphite.send('total', sum(counter.values()))
            if self.params.get('metric_per_ns'):
                graphite.send_dict(counter)
        except Exception as e:
            logging.error('unable to run :: {} :: {}'.format(self.name, e))
            return False
        else:
            logging.info('run :: {} :: send OK'.format(self.name))
            return True
