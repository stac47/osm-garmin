#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Configure the logger used by this application.

Created on 2013-06-24

@author : Laurent Stacul
"""

import logging
import scripts.disttree
import os.path

APP_LOG_FILE = os.path.join(scripts.disttree.LOGGING_DIR, "app.log")


def configLoggers():
    """ Configures the loggers to log into the distribution folder."""

    # First we ensure the dist folder structure is consistant.
    scripts.disttree.createDistDir()

    logger = logging.getLogger("scripts")
    logger.setLevel(logging.DEBUG)

    # This handler will log everything in "dist/log/app.log"
    fileHandler = logging.FileHandler(APP_LOG_FILE, encoding="utf-8")
    fileHandler.setLevel(logging.DEBUG)
    # Create formatter
    formatStr = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    formatter = logging.Formatter(formatStr)

    fileHandler.setFormatter(formatter)

    logger.addHandler(fileHandler)
