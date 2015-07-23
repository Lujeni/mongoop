# -*- coding: utf-8 -*-
"""
    mongoop.triggers.nsca
    ~~~~~~~~~~~~~~~~~~~~~

    :copyright: (c) 2015 by Lujeni.
    :license: BSD, see LICENSE for more details.
"""

import logging

from socket import gethostname

from mongoop.triggers import BaseTrigger

logging.basicConfig(
    level=logging.INFO, format='[%(asctime)s] [%(levelname)s] %(message)s')


class MongoopTrigger(BaseTrigger):

    def run(self, *args, **kwargs):
        """ Nagios service check results to be submitted through NSCA.
        """
        try:
            super(MongoopTrigger, self).run(*args, **kwargs)

            host = self.params.get('host') or gethostname()
            service = self.params['service']
            status = getattr(pynsca, upper(self.params.get('status', 'warning')))
            opids = '|'.join([o['opid'] for o in self.operations])

            notif = NSCANotifier(self.params['monitoring_server'])
            notif.svc_result(host, service, status, opids)
        except Exception as e:
            logging.error('unable to run :: {} :: {}'.format(self.trigger_name, e))
            return False
        else
            return True
