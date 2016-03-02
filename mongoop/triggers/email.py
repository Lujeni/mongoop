# -*- coding: utf-8 -*-
"""
    mongoop.triggers.email
    ~~~~~~~~~~~~~~~~~~~~~~

    :copyright: (c) 2015 by Lujeni.
    :license: BSD, see LICENSE for more details.
"""

from __future__ import absolute_import

import logging
import os

from email.mime.text import MIMEText
from smtplib import SMTP

from jinja2 import Environment
from jinja2 import FileSystemLoader
from jinja2.exceptions import TemplateNotFound

from mongoop.triggers import BaseTrigger


logging.basicConfig(
    level=logging.INFO, format='[%(asctime)s] [%(levelname)s] %(message)s')

PATH = os.path.dirname(os.path.abspath(__file__))

class MongoopTrigger(BaseTrigger):

    def __init__(self, *args, **kwargs):
        super(MongoopTrigger, self).__init__(*args, **kwargs)

        self._jinja_env = Environment(
            autoescape=True,
            loader=FileSystemLoader(os.path.join(PATH, 'templates')),
            trim_blocks=False)
        self._jinja_template_email = self._jinja_env.get_template('email.j2')
        self._jinja_template_balancer = self._jinja_env.get_template('email_balancer.j2')

    def send_email(self, template, context=None):
        try:
            msg_to = self.params['to']
            msg_from = self.params.get('from', 'mongoop@localhost')
            tls = self.params.get('tls', False)
            auth = self.params.get('auth', {})

            msg = MIMEText(template.render(context=context), 'html')
            msg['Subject'] = self.params['subject']
            msg['From'] = msg_from
            msg['To'] = msg_to
            smtp = SMTP(host=self.params['smtp_host'], timeout=10)

            if tls:
                smtp.starttls()

            if auth:
                smtp.login(**auth)

            result = smtp.sendmail(msg_from, [msg_to], msg.as_string())
            smtp.quit()
        except TemplateNotFound as e:
            logging.error('unable to run :: {} :: {}'.format(self.name, e))
            return False
        except Exception as e:
            logging.error('unable to run :: {} :: {}'.format(self.name, e))
            return False
        else:
            logging.info('run :: {} :: send OK'.format(self.name))
            return True

    def op_nok(self, operations):
       self.send_email(template=self._jinja_template_email, context=operations)

    def balancer_nok(self, state):
       self.send_email(template=self._jinja_template_balancer)
