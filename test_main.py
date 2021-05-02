#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `final_project` package."""
from unittest import TestCase
from final_project.visual import linear_regression


class MainProjectLevelTests(TestCase):
    """
    Main project level tests are here.
    """
    def test_main(self):
        """
        This is just to have a main test that just performs a simple assert

        :return:

        """
        linear_regression.visual_demo()
        self.assertTrue(True)
