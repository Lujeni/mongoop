# -*- coding: utf-8 -*-

import sys

import pytest


@pytest.fixture
def base_mongoop_arguments():
    return {
        'mongodb_host': 'localhost',
        'mongodb_port': 27017,
    }

@pytest.fixture
def base_mongoop_trigger_arguments():
    return {
        'name': 'pytest',
        'params': {'threshold': 10},
        'category': 'op'
    }


@pytest.fixture
def base_mongoop(base_mongoop_arguments):
    from mongoop.core import Mongoop

    return Mongoop(**base_mongoop_arguments)


@pytest.fixture
def base_mongoop_trigger(base_mongoop, base_mongoop_trigger_arguments):
    from mongoop.triggers import BaseTrigger
    
    trigger_params = base_mongoop_trigger_arguments
    trigger_params['params']['type'] = 'base'
    trigger_params['mongoop'] = base_mongoop

    return BaseTrigger(**trigger_params)


@pytest.fixture
def email_mongoop_trigger(base_mongoop, base_mongoop_trigger_arguments):
    from mongoop.triggers.email import MongoopTrigger

    trigger_params = base_mongoop_trigger_arguments
    trigger_params['params']['type'] = 'email'
    trigger_params['mongoop'] = base_mongoop
    return MongoopTrigger(**trigger_params)


@pytest.fixture
def killer_mongoop_trigger(base_mongoop, base_mongoop_trigger_arguments):
    from mongoop.triggers.killer import MongoopTrigger
    
    trigger_params = base_mongoop_trigger_arguments
    trigger_params['params']['type'] = 'killer'
    trigger_params['mongoop'] = base_mongoop
    return MongoopTrigger(**trigger_params)


@pytest.fixture
def mongodb_mongoop_trigger(base_mongoop, base_mongoop_trigger_arguments):
    from mongoop.triggers.mongodb import MongoopTrigger

    trigger_params = base_mongoop_trigger_arguments
    trigger_params['params']['type'] = 'mongodb'
    trigger_params['mongoop'] = base_mongoop
    return MongoopTrigger(**trigger_params)


def test_base_trigger_public_api(base_mongoop_trigger):
    assert hasattr(base_mongoop_trigger, 'name')
    assert hasattr(base_mongoop_trigger, 'mongoop')
    assert hasattr(base_mongoop_trigger, 'type')
    assert hasattr(base_mongoop_trigger, 'threshold')
    assert hasattr(base_mongoop_trigger, 'state')
    assert hasattr(base_mongoop_trigger, 'params')
    assert hasattr(base_mongoop_trigger, 'trigger_history')


def test_base_mongoop_public_api(base_mongoop):
    assert hasattr(base_mongoop, '_frequency')
    assert hasattr(base_mongoop, '_mongodb_credentials')
    assert hasattr(base_mongoop, '_mongodb_host')
    assert hasattr(base_mongoop, '_mongodb_options')
    assert hasattr(base_mongoop, '_mongodb_port')
    assert hasattr(base_mongoop, '_query')
    assert hasattr(base_mongoop, '_base_op_query')
    assert hasattr(base_mongoop, '_threshold_timeout')
    assert hasattr(base_mongoop, '_query')

    assert hasattr(base_mongoop, 'conn')
    assert hasattr(base_mongoop, 'db')
    assert hasattr(base_mongoop, 'op_triggers')
    assert hasattr(base_mongoop, 'balancer_triggers')


def test_email_trigger_public_api(email_mongoop_trigger):
    assert hasattr(email_mongoop_trigger, 'name')
    assert hasattr(email_mongoop_trigger, 'mongoop')
    assert hasattr(email_mongoop_trigger, 'type')
    assert hasattr(email_mongoop_trigger, 'category')
    assert hasattr(email_mongoop_trigger, 'threshold')
    assert hasattr(email_mongoop_trigger, 'state')
    assert hasattr(email_mongoop_trigger, 'params')


def test_killer_trigger_public_api(killer_mongoop_trigger):
    assert hasattr(killer_mongoop_trigger, 'name')
    assert hasattr(killer_mongoop_trigger, 'mongoop')
    assert hasattr(killer_mongoop_trigger, 'type')
    assert hasattr(killer_mongoop_trigger, 'category')
    assert hasattr(killer_mongoop_trigger, 'threshold')
    assert hasattr(killer_mongoop_trigger, 'state')
    assert hasattr(killer_mongoop_trigger, 'params')


@pytest.mark.skipif(True, reason='need mongodb instance')
def test_mongodb_trigger_public_api(mongodb_mongoop_trigger):
    assert hasattr(mongodb_mongoop_trigger, 'name')
    assert hasattr(mongodb_mongoop_trigger, 'mongoop')
    assert hasattr(mongodb_mongoop_trigger, 'type')
    assert hasattr(mongodb_mongoop_trigger, 'category')
    assert hasattr(mongodb_mongoop_trigger, 'threshold')
    assert hasattr(mongodb_mongoop_trigger, 'state')
    assert hasattr(mongodb_mongoop_trigger, 'params')
    assert hasattr(mongodb_mongoop_trigger, 'operations')

    assert hasattr(mongodb_mongoop_trigger, 'db')
    assert hasattr(mongodb_mongoop_trigger, 'collection')
