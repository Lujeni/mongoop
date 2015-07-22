# -*- coding: utf-8 -*-

triggers = {
    'mongodb': {
        'threshold': 5,
        'database': 'mongoop',
        'collection': 'history',
    },
    'email': {
        'threshold': 60,
        'subject': 'Mongoop report',
        'from': 'mongoop@localhost',
        'to': 'root',
        'smtp_host': 'localhost',
    },
    'killer': {
        'threshold': 120
    }
}
