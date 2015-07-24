# -*- coding: utf-8 -*-

import pytest


@pytest.fixture
def base_mongoop_arguments():
    return {
        'mongodb_host': 'localhost',
        'mongodb_port': 27017,
        'mongodb_credentials': None,
        'mongodb_options': None,
        'frequency': 60,
        'triggers': {}
    }


@pytest.fixture
def base_mongoop(base_mongoop_arguments):
    from mongoop.core import Mongoop

    return Mongoop(**base_mongoop_arguments)


@pytest.fixture
def base_mongoop_trigger(base_mongoop):
    from mongoop.triggers import BaseTrigger

    return BaseTrigger(trigger_name='pytest', mongoop=base_mongoop, operations={})


def test_base_trigger_public_api(base_mongoop_trigger):
    assert hasattr(base_mongoop_trigger, 'trigger_name')
    assert hasattr(base_mongoop_trigger, 'mongoop')
    assert hasattr(base_mongoop_trigger, 'params')
    assert hasattr(base_mongoop_trigger, '_mix_operations')
    assert hasattr(base_mongoop_trigger, 'operations')


def test_base_mongoop_public_api(base_mongoop):
    assert hasattr(base_mongoop, '_frequency')
    assert hasattr(base_mongoop, '_mongodb_credentials')
    assert hasattr(base_mongoop, '_mongodb_host')
    assert hasattr(base_mongoop, '_mongodb_options')
    assert hasattr(base_mongoop, '_mongodb_port')
    assert hasattr(base_mongoop, '_slow_query')
    assert hasattr(base_mongoop, '_threshold_timeout')

    assert hasattr(base_mongoop, 'conn')
    assert hasattr(base_mongoop, 'db')
    assert hasattr(base_mongoop, 'opid_by_trigger')
    assert hasattr(base_mongoop, 'triggers')
