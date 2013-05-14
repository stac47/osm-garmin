#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Created on 2013-05-14

@author : Laurent Stacul
"""

import unittest
import wrappers


class TestCommandWrapper(unittest.TestCase):

    def test_emptyCommand(self):
        cmd = wrappers.CommandWrapper(command="")
        self.assertEqual("", str(cmd))
        self.assertEqual(1, len(cmd.commandLine))
        self.assertEqual("", cmd.commandLine[0])

    def test_javaCommand(self):
        strCmd = "java -Xmx2048M"
        l = strCmd.split(" ")
        cmd = wrappers.CommandWrapper(command=l[0],
                                      options=[l[1]])
        self.assertEqual(strCmd, str(cmd))
        self.assertEqual(2, len(cmd.commandLine))
        for i in range(2):
            self.assertEqual(l[i], cmd.commandLine[i])
