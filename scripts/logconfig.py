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
    scripts.disttree.create_dist_dir()

    logger = logging.getLogger("scripts")
    logger.setLevel(logging.DEBUG)

    # This handler will log everything in "dist/log/app.log"
    file_handler = logging.FileHandler(APP_LOG_FILE, encoding="utf-8")
    file_handler.setLevel(logging.DEBUG)
    # Create formatter
    format_str = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    formatter = logging.Formatter(format_str)

    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
