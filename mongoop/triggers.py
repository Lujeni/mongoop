# -*- coding: utf-8 -*-
"""
    mongoop.triggers
    ~~~~~~~~~~~~~~~~

    All triggers of mongoop.

    :copyright: (c) 2015 by Lujeni.
    :license: BSD, see LICENSE for more details.
"""

import logging

from email.mime.text import MIMEText
from smtplib import SMTP

from pymongo import DESCENDING
from pymongo.database import Database
from pymongo.errors import DuplicateKeyError


logging.basicConfig(
    level=logging.INFO, format='[%(asctime)s] [%(levelname)s] %(message)s')


__all__ = ['KillerTrigger', 'MongoTrigger', 'EmailTrigger']


# TODO: split the triggers into submodule.
class BaseTrigger(object):

    def __init__(self, mongoop, operations):
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


class KillerTrigger(BaseTrigger):

    def run(self, *args, **kwargs):
        """ Terminates an operation as specified by the operation ID.
        """
        try:
            super(KillerTrigger, self).run(*args, **kwargs)
            # TODO: bulk kill?
            for operation in self.operations:
                opid = operation['opid']
                result = self.mongoop.db.get_collection('$cmd.sys.killop').find_one(
                    {'op': opid})
                logging.info('run :: {} :: {} {}'.format(self.__class__.__name__, result.get('info', 'op'), opid))
        except Exception as e:
            logging.error('unable to run :: {} :: {}'.format(self.__class__.__name__, e))
            return False
        else:
            return True


class MongoTrigger(BaseTrigger):
    """
    TODO: choose/limit the operation fields.
    """

    def __init__(self, *args, **kwargs):
        super(MongoTrigger, self).__init__(*args, **kwargs)

        database = self.mongoop.triggers['mongodb'].get('database', 'mongoop')
        collection = self.mongoop.triggers['mongodb'].get('collection', 'history')

        self.db = Database(self.mongoop.conn, database)
        self.collection = self.db.get_collection(collection)
        self.collection.create_index([('opid', DESCENDING)], unique=True, background=True)

    def run(self, *args, **kwargs):
        try:
            super(MongoTrigger, self).run(*args, **kwargs)

            self.collection.insert_many(self.operations)
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

            email = self.mongoop.triggers['email']
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
