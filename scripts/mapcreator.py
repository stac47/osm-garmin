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

STYLES_DIR = "styles"

# First make sure the java dependencies are available in the disttree.
disttree.update_java_lib()


class MapCreator(object):

    # The default downloader with the default server url
    downloader = None

    # Filepath of downloaded osm files
    downloaded_file_name = []

    # Take the standard mapid for splitter
    last_mapid = 63240001

    def __init__(self, map_xml="map.xml"):
        super().__init__()
        # Load the MapDescriptor from the map.xml
        self.map_descriptor = scripts.mapdescriptor.read_map_xml(map_xml)
        if logger.isEnabledFor(logging.INFO):
            logger.info("Input file: {}".format(map_xml))

    def download(self):
        md = self.map_descriptor
        if len(md.fragments) == 0:
            raise Exception("No Fragment to download")

        if self.downloader is None:
            self.downloader = Downloader(md.download_base_url, 80)

        for fragment in md.fragments:
            filename = fragment.split("/")[-1]
            dst = os.path.join(disttree.GEOFABRIK_LOCAL_DIR, filename)
            self.downloaded_file_name.append(dst)
            self.downloader.add_item(fragment, dst)
        self.downloader.start()

    def __split_map(self, filename):
        cmd_tpl = "java -Xmx1024M -jar %s --mapid=%s --output-dir=%s %s"
        print(cmd_tpl)
        cmd = cmd_tpl % (disttree.SPLITTER_JAR, str(self.last_mapid),
                         disttree.SPLITTER_OUT_DIR, filename)
        if logger.isEnabledFor(logging.DEBUG):
            logger.debug(cmd)
        os.system(cmd)

    def __search_downloaded_files(self):
        self.downloaded_file_name = \
            [os.path.join(disttree.GEOFABRIK_LOCAL_DIR, f)
             for f in os.listdir(disttree.GEOFABRIK_LOCAL_DIR)
             if f.endswith("osm.bz2")]

    def split_maps(self):
        if len(self.downloaded_file_name) == 0:
            self.__search_downloaded_files()
        for f in self.downloaded_file_name:
            if logger.isEnabledFor(logging.DEBUG):
                logger.debug(("%s -> %s" % (f, self.last_mapid)))
            self.__split_map(f)
            self.last_mapid += 100

    def create_maps_from_tiles(self):
        osm_files = [os.path.join(disttree.SPLITTER_OUT_DIR, f)
                     for f in os.listdir(disttree.SPLITTER_OUT_DIR)
                     if f.endswith(".osm.pbf")]
        cmd = wrappers.MkgmapWrapper(jar_path=disttree.MKGMAP_JAR)
        cmd.verbose()
        cmd.output_dir(disttree.MKGMAP_OUT_DIR)
        cmd.index()
        cmd.gmapsupp()
        cmd.family_id(42)
        cmd.family_name("Stac Map")
        cmd.series_name("Stac Series")
        cmd.style_file(STYLES_DIR)
        cmd.style("edge-605-705")
        cmd.remove_short_arcs()
        cmd.generate_sea(["floodblocker"])
        for f in osm_files:
            cmd.input_file(f)
        cmd.input_file(os.path.join(STYLES_DIR, "edge-605-705", "typ.txt"))
        if logger.isEnabledFor(logging.DEBUG):
            logger.debug((str(cmd)))
        os.system(str(cmd))


if __name__ == "__main__":
    pass
