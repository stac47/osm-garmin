#!/usr/bin/env python3
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
import argparse

_parser = argparse.ArgumentParser()
_parser.add_argument("-i", "--inputmap", type=str,
                     help="The input map descriptor file.",
                     default="map.xml")


def main():
    args = _parser.parse_args()
    mp = MapCreator(args.inputmap)
    mp.download()
    mp.split_maps()
    mp.create_maps_from_tiles()


if __name__ == "__main__":
    main()
