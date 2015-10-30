# -*- coding: utf-8 -*-
mongodb_host = 'localhost'

mongodb_port = 27017

mongodb_credentials = None

mongodb_options = None

frequency = 10

threshold_timeout = 60

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
    'sentry': {
        'threshold': 80,
        'dsn': 'https://898weqe899qweqeq8:wqeqw8888@app.getsentry.com/76885',
        'message': 'mongoop slow operation :: {opid}',
        'level': 'info',
    },
    'killer': {
        'threshold': 120
    },
    'webhook': {
        'threshold': 240,
        'method': 'post',
        'url': 'http://requestb.in/17qzafm1',
        'params': {'fizz': 'buzz'},
        'requests_params': {'verify': False},
    }
}
