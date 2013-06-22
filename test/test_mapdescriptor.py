#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Created on 2013-06-22

@author : Laurent Stacul
"""

import scripts.mapdescriptor
import unittest


class TestMapDescriptor(unittest.TestCase):

    def test_getDescriptor(self):
        md = scripts.mapdescriptor.readMapXml("test/res/map.xml")
        self.assertEqual("Map Test", md.title)
        self.assertEqual("1.0", md.version)
        self.assertEqual("stac", md.author)
        self.assertEqual(2, len(md.fragments))
