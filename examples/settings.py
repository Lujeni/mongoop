#!/usr/bin/env python
# vim: set fileencoding=utf-8

triggers = {
    'killer': {'threshold': 120},
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
