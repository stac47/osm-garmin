#!/usr/bin/python3
# vi:set fileencoding=utf-8 :

"""
Created on 2014-03-23

@author : Laurent Stacul
"""

import unittest
import tests.utils


class TestUtils(unittest.TestCase):

    def test_get_test_folder(self):
        test_folder = tests.utils.get_test_folder()
        self.assertEqual("tests", test_folder)
