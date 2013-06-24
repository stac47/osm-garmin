#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Contains pathes and utility functions to manage the folder "dist" which
contains the distribution.

Created on 2013-06-24

@author : Laurent Stacul
"""

import os.path

# Output root folder
DIST_DIR = "dist"

# Output directories
SPLITTER_OUT_DIR = os.path.join(DIST_DIR, "splitter")
MKGMAP_OUT_DIR = os.path.join(DIST_DIR, "mkgmap")

# Local directory where to store files from Geofabrik
GEOFABRIK_LOCAL_DIR = os.path.join(DIST_DIR, "geofabrik")

# Logging directory
LOGGING_DIR = os.path.join(DIST_DIR, "log")


def createDistDir():
    """ Creates the tree for the distribution directory."""

    if not os.path.exists(DIST_DIR):
        os.mkdir(DIST_DIR)
    if not os.path.exists(GEOFABRIK_LOCAL_DIR):
        os.mkdir(GEOFABRIK_LOCAL_DIR)
    if not os.path.exists(SPLITTER_OUT_DIR):
        os.mkdir(SPLITTER_OUT_DIR)
    if not os.path.exists(MKGMAP_OUT_DIR):
        os.mkdir(MKGMAP_OUT_DIR)
    if not os.path.exists(LOGGING_DIR):
        os.mkdir(LOGGING_DIR)
