#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
CLI client application.

TODO:
    - progress bar (http://www.linuxtrack.com/t1171-barre-de-progression.htm)
    - parsing arguments

Created on 2013-06-22

@author : Laurent Stacul
"""

import scripts.logconfig
scripts.logconfig.configLoggers()
from scripts.mapcreator import MapCreator


if __name__ == "__main__":
    mp = MapCreator()
    mp.download()
    mp.split_maps()
    mp.create_maps_from_tiles()
