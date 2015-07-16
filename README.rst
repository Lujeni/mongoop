What is Mongoop ?
=================
Monitor and locate long running operations on MongoDB and automatically trigger specific actions for alerting and performance analysis.

Is it ready ?
=============
It's still not 1.0, missing some features.

TODO
====
::

  trigger :: monitoring (NSCA)
  trigger :: sentry
  trigger :: mongodb :: custom operations field
  trigger :: email :: use a template (jinja)
  core :: python3

Requirements
============

This code has been run on Python 2.7
::

  # install by the setup
  pymongo==3.0.2
  gevent==1.0.2

Usage
=====

Currently, only a cli tool is available:
::

    mongoop


Using your own settings as well:
::

    mongoop --config /path/to/settings.py

Settings
========

Settings are a python file, you can override them easily.
::

    # default
    mongodb_host = 'localhost'

    mongodb_port = 27017

    mongodb_credentials = None

    mongodb_options = None

    frequency = 10

    # the default threshold timeout is set to 60s
    # when no triggers directive is provided.
    triggers = {}

    # sample of  triggers
    triggers = {
        'killer': {
            'threshold': 120
        },
        'email': {
            'threshold': 60,
            'subject': 'Mongoop report',
            'from': 'mongoop@localhost',
            'to': 'root',
            'smtp_host': 'localhost',
        },
        'mongodb': {
            'threshold': 5,
            'database': 'mongoop',
            'collection': 'history'
        }
    }

Triggers
========

Killer
------
Terminates an operation as specified by the operation ID.

MongoDB
--------
Insert the slow OP in a different database and do what you want.

Currently, mongoop use the combo (database/collection).

An index is create on the opid field.

Email
-----
Send an email with each opid.

