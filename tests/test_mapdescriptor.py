#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Created on 2013-06-22

@author : Laurent Stacul
"""

import scripts.mapdescriptor
import unittest
from os.path import join
from tests.utils import get_test_folder


class TestMapDescriptor(unittest.TestCase):

    map_path = join(get_test_folder(), "res", "map.xml")

    def test_get_descriptor(self):
        md = scripts.mapdescriptor.read_map_xml(self.map_path)
        self.assertEqual("Map Test", md.title)
        self.assertEqual("1.0", md.version)
        self.assertEqual("stac", md.author)
        self.assertEqual(2, len(md.fragments))
