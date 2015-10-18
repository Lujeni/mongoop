# -*- coding: utf-8 -*-

import pytest


@pytest.fixture
def base_mongoop_arguments():
    return {
        'mongodb_host': 'localhost',
        'mongodb_port': 27017,
    }


@pytest.fixture
def base_mongoop(base_mongoop_arguments):
    from mongoop.core import Mongoop

    return Mongoop(**base_mongoop_arguments)


@pytest.fixture
def base_mongoop_trigger(base_mongoop):
    from mongoop.triggers import BaseTrigger

    return BaseTrigger(trigger_name='pytest', mongoop=base_mongoop, operations={})


@pytest.fixture
def email_mongoop_trigger(base_mongoop):
    from mongoop.triggers.email import MongoopTrigger

    return MongoopTrigger(trigger_name='pytest', mongoop=base_mongoop, operations={})


@pytest.fixture
def killer_mongoop_trigger(base_mongoop):
    from mongoop.triggers.killer import MongoopTrigger

    return MongoopTrigger(trigger_name='pytest', mongoop=base_mongoop, operations={})


@pytest.fixture
def mongodb_mongoop_trigger(base_mongoop):
    from mongoop.triggers.mongodb import MongoopTrigger

    return MongoopTrigger(trigger_name='pytest', mongoop=base_mongoop, operations={})


@pytest.fixture
def nsca_mongoop_trigger(base_mongoop):
    from mongoop.triggers.mongodb import MongoopTrigger

    return MongoopTrigger(trigger_name='pytest', mongoop=base_mongoop, operations={})


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


def test_email_trigger_public_api(email_mongoop_trigger):
    assert hasattr(email_mongoop_trigger, 'trigger_name')
    assert hasattr(email_mongoop_trigger, 'mongoop')
    assert hasattr(email_mongoop_trigger, 'params')
    assert hasattr(email_mongoop_trigger, '_mix_operations')
    assert hasattr(email_mongoop_trigger, 'operations')


def test_killer_trigger_public_api(killer_mongoop_trigger):
    assert hasattr(killer_mongoop_trigger, 'trigger_name')
    assert hasattr(killer_mongoop_trigger, 'mongoop')
    assert hasattr(killer_mongoop_trigger, 'params')
    assert hasattr(killer_mongoop_trigger, '_mix_operations')
    assert hasattr(killer_mongoop_trigger, 'operations')

@pytest.mark.mongodb
def test_mongodb_trigger_public_api(mongodb_mongoop_trigger):
    assert hasattr(mongodb_mongoop_trigger, 'trigger_name')
    assert hasattr(mongodb_mongoop_trigger, 'mongoop')
    assert hasattr(mongodb_mongoop_trigger, 'params')
    assert hasattr(mongodb_mongoop_trigger, '_mix_operations')
    assert hasattr(mongodb_mongoop_trigger, 'operations')

    assert hasattr(mongodb_mongoop_trigger, 'db')
    assert hasattr(mongodb_mongoop_trigger, 'collection')


def test_nsca_trigger_public_api(nsca_mongoop_trigger):
    assert hasattr(nsca_mongoop_trigger, 'trigger_name')
    assert hasattr(nsca_mongoop_trigger, 'mongoop')
    assert hasattr(nsca_mongoop_trigger, 'params')
    assert hasattr(nsca_mongoop_trigger, '_mix_operations')
    assert hasattr(nsca_mongoop_trigger, 'operations')
