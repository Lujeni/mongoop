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

Configure your Mongoop settings:

- `Settings file <https://github.com/lujeni/mongoop/wiki/Settings-File>`_

List of available triggers:

- `List of available triggers <https://github.com/lujeni/mongoop/wiki/Available-Triggers>`_

Learn how to write your own triggers:

- `Write your own triggers <https://github.com/lujeni/mongoop/wiki/Write-your-own-triggers>`_

Usage
=====
Currently, mongoop is a simple cli tool:
::
    $ mongoop


Using your own settings as well:
::

    $ mongoop --config /path/to/settings.py
    $ mongoop --config /path/to/settings.yaml


Requirements
============
This code has been run on Python 2.7
::

  # install by the setup
  Jinja2==2.8
  PyYAML==3.11
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
