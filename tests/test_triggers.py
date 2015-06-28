#!/usr/bin/env python
# vim: set fileencoding=utf-8

import unittest

from mongoop.triggers import BaseTrigger


class TestBasetrigger(unittest.TestCase):

    def test_public_api(self):
        self.assertTrue(hasattr(BaseTrigger, 'pre_run'))
        self.assertTrue(hasattr(BaseTrigger, 'post_run'))
        self.assertTrue(hasattr(BaseTrigger, 'run'))
