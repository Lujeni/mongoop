#!/usr/bin/env python
# vim: set fileencoding=utf-8

# DEFAULT MONGODB
mongodb_host = 'localhost'

mongodb_port = 27017

mongodb_credentials = None

mongodb_options = None

# DEFAULT MONGOOP
mongoop_running_timeout = 120

mongoop_frequency = 10

mongoop_killer = True

mongoop_trigger = []

# DEFAULT MONGOOP TRIGGER
mongoop_trigger_email = {
    'subject': 'Mongoop report',
    'from': 'mongoop@localhost',
    'to': 'root',
    'smtp_host': 'localhost',
}
