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
import shutil
import logging
logger = logging.getLogger(__name__)

import scripts.wrappers as wrappers
from scripts.httputils import Downloader
import scripts.disttree as disttree
import scripts.mapdescriptor

STYLES_DIR = "styles"

# First make sure the java dependencies are available in the disttree.
# disttree.update_java_lib()

def download(map_xml='map.xml'):
    map_descriptor = scripts.mapdescriptor.read_map_xml(map_xml)
    if len(map_descriptor.fragments) == 0:
        raise Exception("No Fragment to download")

    downloader = Downloader(map_descriptor.download_base_url, 80)

    for fragment in map_descriptor.fragments:
        filename = fragment.split("/")[-1]
        dst = os.path.join(disttree.GEOFABRIK_LOCAL_DIR, filename)
        if not os.path.exists(dst):
            downloader.add_item(fragment, dst)
    return downloader.start()


def __split_map(filename, mapid):
    cmd_tpl = "java -Xmx1024M -jar %s --mapid=%s --output-dir=%s %s"
    cmd = cmd_tpl % (disttree.SPLITTER_JAR, str(mapid),
                     disttree.SPLITTER_OUT_DIR, filename)
    if logger.isEnabledFor(logging.DEBUG):
        logger.debug(cmd)
    os.system(cmd)


def __search_downloaded_files():
    downloaded_file_name = \
        [os.path.join(disttree.GEOFABRIK_LOCAL_DIR, f)
         for f in os.listdir(disttree.GEOFABRIK_LOCAL_DIR)
         if f.endswith("osm.bz2")]
    return downloaded_file_name


def split_maps():
    # Remove the previous tiles
    shutil.rmtree(disttree.SPLITTER_OUT_DIR)
    disttree.create()
    mapid = 63240001
    downloaded_file_name =  __search_downloaded_files()
    for f in downloaded_file_name:
        if logger.isEnabledFor(logging.DEBUG):
            logger.debug(("%s -> %s" % (f, mapid)))
        __split_map(f, mapid)
        mapid += 100


def create_map_from_tiles():
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
    cmd.style("garmin-edge")
    cmd.remove_short_arcs()
    cmd.generate_sea(["floodblocker"])
    for f in osm_files:
        cmd.input_file(f)
    cmd.input_file(os.path.join(STYLES_DIR, "garmin-edge", "typ.txt"))
    if logger.isEnabledFor(logging.DEBUG):
        logger.debug((str(cmd)))
    os.system(str(cmd))
