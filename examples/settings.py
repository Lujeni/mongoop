# -*- coding: utf-8 -*-

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
        'threshold': 60,
        'monitoring_server': 'nagios.foo.com',
        'service': 'mongoop',
        'status': 'critical',
    },
    'email': {
        'threshold': 60,
        'subject': 'Mongoop report',
        'from': 'mongoop@localhost',
        'to': 'root',
        'smtp_host': 'localhost',
    },
    'email': {
        'threshold': 60,
        'subject': 'Mongoop report',
        'from': 'mongoop@localhost',
        'to': 'sysadmin',
        'smtp_host': 'smtp.gmail.com:587',
        'gmail': {'user': 'foo', 'password': 'bar'}
    },
    'killer': {
        'threshold': 120
    }
}
