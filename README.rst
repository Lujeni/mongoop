Mongoop
=======

Introduction
============
This tool can be used to locate long running operations and trigger an specific action.


TODO
====
::

  # v0.1
  unittests

  # v0.2
  quiet logging option
  web interface
  monitoring trigger (NSCA)

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

Your own settings is just a simple override of the default settings:
::

    # DEFAULT MONGODB
    mongodb_host = 'localhost'

    mongodb_port = 27017

    mongodb_credentials = None
    mongodb_credentials = {'name': 'foo', 'password': 'bar'}

    mongodb_options = None
    mongodb_options = {'ssl': True}

    # DEFAULT MONGOOP
    mongoop_running_timeout = 120

    mongoop_frequency = 10

    # let mongoop try to kill the slow operations.
    mongoop_killer = True

    # trigger action after detect an slow operation.
    mongoop_trigger = []
    mongoop_trigger = ['mongodb']
    mongoop_trigger = ['email']

    # DEFAULT MONGOOP TRIGGER
    mongoop_trigger_email = {
      'subject': 'Mongoop report',
      'from': 'mongoop@localhost',
      'to': 'root',
      'smtp_host': 'localhost'
    }

Triggers
========

=======
MongoDB
=======

introduction
------------

Insert the slow OP in a different database and do what you want.

Currently, mongoop use the combo mongoop/history (database/collection).

An index is create on the opid field.

todo
----

::

  database/collection combo must be a settings.
  credentials on this database is not support.
  choose/limit the operations fields which are inserted.

=====
Email
=====

introduction
------------

Send an email with each opid.

todo
----

::

  templating (jinja2)
