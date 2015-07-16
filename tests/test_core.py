#!/usr/bin/env python
# vim: set fileencoding=utf-8

import pytest

from mongoop.core import Mongoop


@pytest.fixture()
def base_mongoop_arguments():
    return {
        'mongodb_host': 'localhost',
        'mongodb_port': 27017,
        'mongodb_credentials': None,
        'mongodb_options': None,
        'frequency': 60,
        'triggers': {}
    }


@pytest.fixture()
def base_mongoop(base_mongoop_arguments):
    return MongoOP(**base_mongoop_arguments)


def test_base_init(base_mongoop):
    assert hasattr(base_mongoop, 'mongodb_host')
    assert hasattr(base_mongoop, 'mongodb_port')
    assert hasattr(base_mongoop, 'mongodb_credentials')
    assert hasattr(base_mongoop, 'mongodb_options')

