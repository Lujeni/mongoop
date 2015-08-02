What is Mongoop ?
=================
Monitor and locate long running operations on MongoDB and automatically trigger specific actions for alerting and performance analysis.

Is it ready ?
=============
It's still not 1.0 but enought mature to test on your infrastructure.

Documentation
=============
Up to date documentation:

- `See the wiki <https://github.com/lujeni/mongoop/wiki>`_

List of avaiable triggers:

- `List of available triggers <https://github.com/lujeni/mongoop/wiki/avaiable-triggers>`

Learn how to write your own triggers:

- `Write your own triggers <https://github.com/lujeni/mongoop/wiki/Write-your-own-triggers>`_

Usage
=====
Currently, mongoop is a simple cli tool:
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
        'mongodb': {
            'threshold': 5,
            'database': 'mongoop',
            'collection': 'history',
        },
        'nsca': {
            'threshold': 5,
            'monitoring_server': 'nagios.foo.com',
            'service': 'mongoop',
        },
        'nsca': {
            'threshold': 30,
            'monitoring_server': 'nagios.foo.com',
            'service': 'mongoop',
            'status': 'critical',
        },
        'email': {
            'threshold': 30,
            'subject': 'Mongoop report',
            'from': 'mongoop@localhost',
            'to': 'root',
            'smtp_host': 'localhost',
        },
        'sentry': {
            'threshold': 60,
            'dsn': 'https://898weqe899qweqeq8:wqeqw8888@app.getsentry.com/76885',
            'message': 'mongoop slow operation :: {opid}',
            'level': 'info',
        },
        'killer': {
            'threshold': 120
        }
    }


Requirements
============
This code has been run on Python 2.7
::

  # install by the setup
  Jinja2==2.8
  gevent==1.0.2
  pymongo==3.0.2
  pynsca==1.5

Installation
============
Pypi
----
Using pip:
::

    $ pip install mongoop

Gentoo Linux
------------
Using emerge (very soon):
::

    $ sudo emerge -a mongoop
