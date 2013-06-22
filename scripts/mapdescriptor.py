#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Created on 2013-06-22

@author : Laurent Stacul
"""

import xml.etree.ElementTree as ET


DEFAULT_MAP = "map.xml"


class MapDescriptor(object):

    title = "MyMap"
    author = "Nobody"
    version = "0.1"
    fragments = []


def readMapXml(source=DEFAULT_MAP):
    ret = MapDescriptor()
    tree = ET.ElementTree()
    tree.parse(source)

    # Parsing general information
    ret.title = tree.find("title").text
    ret.author = tree.find("author").text
    ret.version = tree.find("version").text

    # Getting the urls of the source files
    for e in tree.iterfind("fragments/fragment"):
        ret.fragments.append(e.attrib["src"])
    return ret
