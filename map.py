#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Created on 2013-06-22

@author : Laurent Stacul
"""

import scripts.pymapcreator

if __name__ == "__main__":
    mp = scripts.pymapcreator.MapCreator()
    mp.createDistDir()
    mp.download()
    mp.splitMaps()
    mp.createMapsFromTiles()
