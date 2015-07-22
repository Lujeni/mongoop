# -*- coding: utf-8 -*-
"""
    mongoop.triggers.email
    ~~~~~~~~~~~~~~~~~~~~~~

    :copyright: (c) 2015 by Lujeni.
    :license: BSD, see LICENSE for more details.
"""

import logging

from email.mime.text import MIMEText
from smtplib import SMTP

from mongoop.triggers import BaseTrigger


logging.basicConfig(
    level=logging.INFO, format='[%(asctime)s] [%(levelname)s] %(message)s')


class MongoopTrigger(BaseTrigger):

    def run(self, *args, **kwargs):
        try:
            super(MongoopTrigger, self).run(*args, **kwargs)

            email = self.mongoop.triggers['email']
            msg_from = email['from']
            msg_to = email['to']

            msg = MIMEText(' \n'.join(['opipd: {}'.format(str(o['opid']))
                                       for o in self.operations]))
            msg['Subject'] = email['subject']
            msg['From'] = msg_from
            msg['To'] = msg_to

            smtp = SMTP(host=email['smtp_host'], timeout=10)
            smtp.sendmail(msg_from, [msg_to], msg.as_string())
            smtp.quit()
        except Exception as e:
            logging.error('unable to run :: {} :: {}'.format(self.__class__.__name__, e))
            return False
        else:
            return True

