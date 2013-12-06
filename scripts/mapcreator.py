#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Created on 2011-08-01

@author : Laurent Stacul

This script aims at creating map for garmin edge.
1 - Download raw map data from OSM repository
2 - Split each map
3 - Create the final result to be uploaded onto garmin device.
"""

import os
import os.path
import scripts.wrappers as wrappers
from scripts.httputils import Downloader
import scripts.disttree as disttree
import scripts.mapdescriptor
import logging
logger = logging.getLogger(__name__)

# Reflects the structure of the project
LIB_DIR = "lib"
STYLES_DIR = "styles"

# Name of splitter directory (used for lib and output)
SPLITTER_DIR = "splitter"

# Name of mkgmap directory (used for lib and output)
MKGMAP_DIR = "mkgmap"

# Path to Splitter JAR (tiles creator)
SPLITTER_JAR = os.path.join(LIB_DIR, SPLITTER_DIR, "splitter.jar")

# Path to mkgmap Jar (map creator)
MKGMAP_JAR = os.path.join(LIB_DIR, MKGMAP_DIR, "mkgmap.jar")


class MapCreator(object):

    # The default downloader with the default server url
    downloader = None

    # Filepath of downloaded osm files
    downloadedFileName = []

    # Take the standard mapid for splitter
    lastMapid = 63240001

    def __init__(self, mapXml="map.xml"):
        super().__init__()
        # Load the MapDescriptor from the map.xml
        self.mapDescriptor = scripts.mapdescriptor.readMapXml()

    def download(self):
        md = self.mapDescriptor
        if len(md.fragments) == 0:
            raise Exception("No Fragment to download")

        if self.downloader is None:
            self.downloader = Downloader(md.downloadBaseUrl, 80)

        for fragment in md.fragments:
            filename = fragment.split("/")[-1]
            dst = os.path.join(disttree.GEOFABRIK_LOCAL_DIR, filename)
            self.downloadedFileName.append(dst)
            self.downloader.addItem(fragment, dst)
        self.downloader.start()

    def __splitMap(self, filename):
        cmdTpl = "java -Xmx1024M -jar %s --mapid=%s --output-dir=%s %s"
        print(cmdTpl)
        cmd = cmdTpl % (SPLITTER_JAR, str(self.lastMapid),
                        disttree.SPLITTER_OUT_DIR, filename)
        if logger.isEnabledFor(logging.DEBUG):
            logger.debug(cmd)
        os.system(cmd)

    def __searchDownloadedFiles(self):
        self.downloadedFileName = \
            [os.path.join(disttree.GEOFABRIK_LOCAL_DIR, f)
             for f in os.listdir(disttree.GEOFABRIK_LOCAL_DIR)
             if f.endswith("osm.bz2")]

    def splitMaps(self):
        if len(self.downloadedFileName) == 0:
            self.__searchDownloadedFiles()
        for f in self.downloadedFileName:
            if logger.isEnabledFor(logging.DEBUG):
                logger.debug(("%s -> %s" % (f, self.lastMapid)))
            self.__splitMap(f)
            self.lastMapid += 100

    def createMapsFromTiles(self):
        osmFiles = [os.path.join(disttree.SPLITTER_OUT_DIR, f)
                    for f in os.listdir(disttree.SPLITTER_OUT_DIR)
                    if f.endswith(".osm.pbf")]
        cmd = wrappers.MkgmapWrapper(jarPath=MKGMAP_JAR)
        cmd.verbose()
        cmd.outputDir(disttree.MKGMAP_OUT_DIR)
        cmd.index()
        cmd.gmapsupp()
        cmd.familyId(42)
        cmd.familyName("Stac Map")
        cmd.seriesName("Stac Series")
        cmd.styleFile(STYLES_DIR)
        cmd.style("edge-605-705")
        cmd.removeShortArcs()
        cmd.generateSea(["floodblocker"])
        for f in osmFiles:
            cmd.inputFile(f)
        cmd.inputFile(os.path.join(STYLES_DIR, "edge-605-705", "typ.txt"))
        if logger.isEnabledFor(logging.DEBUG):
            logger.debug((str(cmd)))
        os.system(str(cmd))


if __name__ == "__main__":
    pass
