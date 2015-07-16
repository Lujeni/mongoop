#!/usr/bin/env python
# vim: set fileencoding=utf-8


from mongoop.triggers import BaseTrigger


def test_public_api():
    assert hasattr(BaseTrigger, 'pre_run')
    assert hasattr(BaseTrigger, 'post_run')
    assert hasattr(BaseTrigger, 'run')

