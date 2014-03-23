#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Created on 2013-05-14

@author : Laurent Stacul
"""

import unittest
import scripts.wrappers as wrappers


class TestCommandWrapper(unittest.TestCase):

    def test_empty_command(self):
        cmd = wrappers.CommandWrapper(command="")
        self.assertEqual("", str(cmd))
        self.assertEqual(1, len(cmd.command_line))
        self.assertEqual("", cmd.command_line[0])

    def test_java_command(self):
        str_cmd = "java -Xmx2048M"
        l = str_cmd.split(" ")
        cmd = wrappers.CommandWrapper(command=l[0],
                                      options=[l[1]])
        self.assertEqual(str_cmd, str(cmd))
        self.assertEqual(2, len(cmd.command_line))
        for i in range(2):
            self.assertEqual(l[i], cmd.command_line[i])
