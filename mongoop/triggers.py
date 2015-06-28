#!/usr/bin/env python
# vim: set fileencoding=utf-8

import logging

from email.mime.text import MIMEText
from smtplib import SMTP

from pymongo import DESCENDING
from pymongo.database import Database
from pymongo.errors import DuplicateKeyError


logging.basicConfig(
    level=logging.INFO, format='[%(asctime)s] [%(levelname)s] %(message)s')


__all__ = ['MongoTrigger', 'EmailTrigger']


class BaseTrigger(object):

    def __init__(self, mongoop, operations):
        self.trigger_in_progress = set()
        self.mongoop = mongoop
        self.operations = operations

    def pre_run(self, *args, **kwargs):
        pass

    def post_run(self, *args, **kwargs):
        pass

    def run(self, *args, **kwargs):
        logging.info('run :: {}'.format(self.__class__.__name__))

    def __call__(self, *args, **kwargs):
        self.pre_run(*args, **kwargs)
        self.run(*args, **kwargs)
        self.post_run(*args, **kwargs)


class MongoTrigger(BaseTrigger):
    """
    TODO: database options could be customizable.
    TODO: conn could be use through credentials.
    TODO: choose/limit the operation fields.
    """

    def __init__(self, *args, **kwargs):
        super(MongoTrigger, self).__init__(*args, **kwargs)

        self.db = Database(self.mongoop.conn, 'mongoop')
        self.db.history.create_index([('opid', DESCENDING)], unique=True, background=True)

    def run(self, *args, **kwargs):
        try:
            super(MongoTrigger, self).run(*args, **kwargs)

            if self.operations:
                self.db.history.insert_many(self.operations)
        except DuplicateKeyError as e:
            logging.debug('op already trigger :: {}'.format(e))
        except Exception as e:
            logging.error('unable to run :: {} :: {}'.format(self.__class__.__name__, e))
            return False
        else:
            return True


class EmailTrigger(BaseTrigger):
    """
    TODO: using a templating (jinja)
    """

    def run(self, *args, **kwargs):
        try:
            super(EmailTrigger, self).run(*args, **kwargs)

            email = self.mongoop.mongoop_trigger_email
            msg_from = email['from']
            msg_to = email['to']

            msg = MIMEText(' \n'.join(['opipd: {}'.format(str(o['opid'])) for o in self.operations]))
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
