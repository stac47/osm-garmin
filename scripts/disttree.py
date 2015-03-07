#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Contains pathes and utility functions to manage the folder "dist" which
contains the distribution.

Created on 2013-06-24

@author : Laurent Stacul
"""

import os.path
import shutil
import logging
from scripts.httputils import Downloader
from zipfile import ZipFile
logger = logging.getLogger(__name__)

# Output root folder
DIST_DIR = "dist"

# Output directories
SPLITTER_OUT_DIR = os.path.join(DIST_DIR, "splitter")
MKGMAP_OUT_DIR = os.path.join(DIST_DIR, "mkgmap")

# Local directory where to store files from Geofabrik
GEOFABRIK_LOCAL_DIR = os.path.join(DIST_DIR, "geofabrik")

# Logging directory
LOGGING_DIR = os.path.join(DIST_DIR, "log")

# Directory to store mkgmap & splitter
JAVA_LIB_DIR = os.path.join(DIST_DIR, "lib")
JAVA_LIB_SOURCE_URL = "http://www.mkgmap.org.uk"

# Splitter
SPLITTER_VERSION = "splitter-r421"
SPLITTER_DIR = os.path.join(JAVA_LIB_DIR, SPLITTER_VERSION)
SPLITTER_ZIP = SPLITTER_VERSION + ".zip"
SPLITTER_JAR = os.path.join(SPLITTER_DIR, "splitter.jar")

# Mkgmap Version
MKGMAP_VERSION = "mkgmap-r3491"
MKGMAP_DIR = os.path.join(JAVA_LIB_DIR, MKGMAP_VERSION)
MKGMAP_ZIP = MKGMAP_VERSION + ".zip"
MKGMAP_JAR = os.path.join(MKGMAP_DIR, "mkgmap.jar")


_downloader = Downloader(JAVA_LIB_SOURCE_URL)


def create():
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
    if not os.path.exists(JAVA_LIB_DIR):
        os.mkdir(JAVA_LIB_DIR)


def clean():
    """ Delete the content of the distribution tree except the lib folder."""
    shutil.rmtree(GEOFABRIK_LOCAL_DIR)
    shutil.rmtree(SPLITTER_OUT_DIR)
    shutil.rmtree(MKGMAP_OUT_DIR)
    shutil.rmtree(LOGGING_DIR)
    create()


def update_java_lib():
    """ Tests if the java libs are present and their version, and if
    needed, download and inflate them."""

    if not os.path.exists(DIST_DIR):
        create()
    files_to_download = []
    if not os.path.exists(MKGMAP_DIR):
        files_to_download.append(MKGMAP_ZIP)
    if not os.path.exists(SPLITTER_DIR):
        files_to_download.append(SPLITTER_ZIP)
    if len(files_to_download) > 0:
        for f in files_to_download:
            logger.info("%s to be updated" % f)
            _downloader.add_item("/download/" + f,
                                 os.path.join(JAVA_LIB_DIR, f))
        _downloader.start()
    elif logger.isEnabledFor(logging.INFO):
        logger.info("Java dependencies are up-to-date.")
    with ZipFile(os.path.join(JAVA_LIB_DIR, SPLITTER_ZIP), "r") as f:
        f.extractall(JAVA_LIB_DIR)
    with ZipFile(os.path.join(JAVA_LIB_DIR, MKGMAP_ZIP), "r") as f:
        f.extractall(JAVA_LIB_DIR)


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    create()
    update_java_lib()
