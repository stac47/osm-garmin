#!/usr/bin/env python3
# vi:set fileencoding=utf-8 :

"""
Created on 2014-03-22

@author : Laurent Stacul
"""

import unittest
import os
import os.path
import shutil
import scripts.disttree
import scripts.disttree as disttree
from urllib.parse import urlparse
from zipfile import ZipFile


class MockDownloader(object):
    """ Emulates Downloader dedicated to the download of java dependencies."""

    def __init__(self):
        super().__init__()
        self._items = dict()
        self.number_downloaded_files = 0

    def add_item(self, resource_uri, dst):
        self._items[resource_uri] = dst

    def start(self):
        for k, v in self._items.items():
            parsed_url = urlparse(k)
            file_name = parsed_url.path.split("/")[-1]
            with ZipFile(v, 'w') as f:
                basename = file_name.split(".")[0]
                f.write(__file__,
                        os.path.join(basename,
                                     basename.split("-")[0] + ".jar"))
                self.number_downloaded_files += 1


class TestDistTree(unittest.TestCase):

    def setUp(self):
        self.saved_cwd = os.getcwd()
        os.chdir(os.path.dirname(__file__))
        # Do not download for real
        self.downloader = MockDownloader()
        scripts.disttree._downloader = self.downloader

    def test_disttree_creation(self):
        self.assertEqual(0, self.downloader.number_downloaded_files)
        disttree.create()
        self.assertEqual(0, self.downloader.number_downloaded_files)
        disttree.update_java_lib()
        self.assertEqual(2, self.downloader.number_downloaded_files)
        self.assertTrue(os.path.exists(scripts.disttree.DIST_DIR))
        self.assertTrue(os.path.exists(scripts.disttree.SPLITTER_OUT_DIR))
        self.assertTrue(os.path.exists(scripts.disttree.MKGMAP_OUT_DIR))
        self.assertTrue(os.path.exists(scripts.disttree.GEOFABRIK_LOCAL_DIR))
        self.assertTrue(os.path.exists(scripts.disttree.LOGGING_DIR))
        self.assertTrue(os.path.exists(scripts.disttree.JAVA_LIB_DIR))
        mkgmap_zip = os.path.join(scripts.disttree.JAVA_LIB_DIR,
                                  scripts.disttree.MKGMAP_ZIP)
        self.assertTrue(os.path.exists(mkgmap_zip))
        splitter_zip = os.path.join(scripts.disttree.JAVA_LIB_DIR,
                                    scripts.disttree.SPLITTER_ZIP)
        self.assertTrue(splitter_zip)
        self.assertTrue(os.path.exists(scripts.disttree.SPLITTER_DIR))
        self.assertTrue(os.path.exists(scripts.disttree.MKGMAP_DIR))
        self.assertTrue(os.path.exists(scripts.disttree.SPLITTER_JAR))
        self.assertTrue(os.path.exists(scripts.disttree.MKGMAP_JAR))

        # If we try again to build the disttree, no download of the jars
        disttree.update_java_lib()
        self.assertEqual(2, self.downloader.number_downloaded_files)

        # Cleaning the dist folder
        disttree.clean()
        # All folders exist
        self.assertTrue(os.path.exists(scripts.disttree.DIST_DIR))
        self.assertTrue(os.path.exists(scripts.disttree.SPLITTER_OUT_DIR))
        self.assertTrue(os.path.exists(scripts.disttree.MKGMAP_OUT_DIR))
        self.assertTrue(os.path.exists(scripts.disttree.GEOFABRIK_LOCAL_DIR))
        # The java libs have not been deleted so no download done.
        disttree.update_java_lib()
        self.assertEqual(2, self.downloader.number_downloaded_files)

    def tearDown(self):
        shutil.rmtree(scripts.disttree.DIST_DIR)
        os.chdir(self.saved_cwd)
        scripts.disttree._downloader = None
