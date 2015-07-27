# -*- coding: utf-8 -*-
"""
    mongoop.triggers.email
    ~~~~~~~~~~~~~~~~~~~~~~

    :copyright: (c) 2015 by Lujeni.
    :license: BSD, see LICENSE for more details.
"""

from __future__ import absolute_import

import logging

from email.mime.text import MIMEText
from smtplib import SMTP

from mongoop.triggers import BaseTrigger


logging.basicConfig(
    level=logging.INFO, format='[%(asctime)s] [%(levelname)s] %(message)s')


class MongoopTrigger(BaseTrigger):

    def run(self):
        try:
            msg_from = self.params['from']
            msg_to = self.params['to']

            msg = MIMEText(' \n'.join(['opipd: {}'.format(str(o['opid']))
                                       for o in self.operations]))
            msg['Subject'] = self.params['subject']
            msg['From'] = msg_from
            msg['To'] = msg_to

            smtp = SMTP(host=self.params['smtp_host'], timeout=10)
            smtp.sendmail(msg_from, [msg_to], msg.as_string())
            smtp.quit()
        except Exception as e:
            logging.error('unable to run :: {} :: {}'.format(self.trigger_name, e))
            return False
        else:
            return True
