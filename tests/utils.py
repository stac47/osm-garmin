#!/usr/bin/python3
# vi:set fileencoding=utf-8 :

"""
Created on 2014-03-23

@author : Laurent Stacul
"""

import os.path


def get_test_folder():
    """ Returns the current tests folder."""

    current_dir = os.path.dirname(__file__)
    _, tail = os.path.split(current_dir)
    return tail
