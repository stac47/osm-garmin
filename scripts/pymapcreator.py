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
import wrappers

# Reflects the structure of the project
LIB_DIR = "lib"
DIST_DIR = "dist"
STYLES_DIR = "styles"

# Geofabrik URLs
GEOFABRIK_BASE_URL = "http://download.geofabrik.de/"
GEOFABRIK_EUROPE_URL = GEOFABRIK_BASE_URL + "europe/"
GEOFABRIK_FRANCE_URL = GEOFABRIK_EUROPE_URL + "france/"

# Local directory where to store files from Geofabrik
GEOFABRIK_LOCAL_DIR = os.path.join(DIST_DIR, "geofabrik")

# From geofabrik we will take only the *.osm.bz2 files (not pbf nor shp files)
EXTENSION = "-latest.osm.bz2"

# Region of France
ALSACE = "alsace"
AQUITAINE = "aquitaine"
AUVERGNE = "auvergne"
BASSE_NORMANDIE = "basse-normandie"
BOURGOGNE = "bourgogne"
BRETAGNE = "bretagne"
CENTRE = "centre"
CHAMPAGNE_ARDENNE = "champagne-ardenne"
CORSE = "corse"
FRANCHE_COMTE = "franche-comte"
HAUTE_NORMANDIE = "haute-normandie"
ILE_DE_FRANCE = "ile-de-france"
LANGUEDOC_ROUSSILLON = "languedoc-roussillon"
LIMOUSIN = "limousin"
LORRAINE = "lorraine"
MIDI_PYRENEES = "midi-pyrenees"
NORD_PAS_DE_CALAIS = "nord-pas-de-calais"
PAYS_DE_LA_LOIRE = "pays-de-la-loire"
PICARDIE = "picardie"
POITOU_CHARENTES = "poitou-charentes"
PROVENCE_ALPES_COTE_D_AZUR = "provence-alpes-cote-d-azur"
RHONE_ALPES = "rhone-alpes"

# By default, we'll take of files from France
DEFAULT_OSM_FILES = [PROVENCE_ALPES_COTE_D_AZUR, RHONE_ALPES,
                     LANGUEDOC_ROUSSILLON, MIDI_PYRENEES, AQUITAINE,
                     AUVERGNE, CORSE]

SPLITTER_DIR = "splitter"

MKGMAP_DIR = "mkgmap"

# Path to Splitter JAR (tiles creator)
SPLITTER_JAR = os.path.join(LIB_DIR, SPLITTER_DIR, "splitter.jar")
SPLITTER_OUT_DIR = os.path.join(DIST_DIR, SPLITTER_DIR)

# Path to mkgmap Jar (map creator)
MKGMAP_JAR = os.path.join(LIB_DIR, MKGMAP_DIR, "mkgmap.jar")
MKGMAP_OUT_DIR = os.path.join(DIST_DIR, MKGMAP_DIR)


def createDistDir():
    if not os.path.exists(DIST_DIR):
        os.mkdir(DIST_DIR)
    if not os.path.exists(GEOFABRIK_LOCAL_DIR):
        os.mkdir(GEOFABRIK_LOCAL_DIR)
    if not os.path.exists(SPLITTER_OUT_DIR):
        os.mkdir(SPLITTER_OUT_DIR)
    if not os.path.exists(MKGMAP_OUT_DIR):
        os.mkdir(MKGMAP_OUT_DIR)


def download(l=DEFAULT_OSM_FILES):
    cmd = "wget %s -O %s"
    for filename in l:
        src = GEOFABRIK_FRANCE_URL + filename + EXTENSION
        dst = os.path.join(GEOFABRIK_LOCAL_DIR, filename + EXTENSION)
        os.system(cmd % (src, dst))


def splitMap(filename, mapid=63240001):
    filepath = os.path.join(GEOFABRIK_LOCAL_DIR, filename + EXTENSION)
    cmd = "java -Xmx2048M -jar %s --mapid=%s --output-dir=%s %s"
    os.system(cmd % (SPLITTER_JAR, str(mapid),
                     SPLITTER_OUT_DIR, filepath))


def createMapsFromTiles():
    osmFiles = [os.path.join(SPLITTER_OUT_DIR, f)
                for f in os.listdir(SPLITTER_OUT_DIR)
                if f.endswith(".osm.pbf")]
    cmd = wrappers.MkgmapWrapper(jarPath=MKGMAP_JAR)
    cmd.verbose()
    cmd.outputDir(MKGMAP_OUT_DIR)
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
    print(str(cmd))
    os.system(str(cmd))


def splitMaps(l):
    mapidBase = 63240001
    for f in l:
        print(("%s -> %s" % (f, mapidBase)))
        splitMap(f, mapidBase)
        mapidBase += 100


def fullProcess(l=DEFAULT_OSM_FILES):
    """ Generates a map of France to be uploaded onto Garmin device. Output
    file is 'gmapsupp.img'.
    """

    createDistDir()
    download(DEFAULT_OSM_FILES[0:1])
    createMapsFromTiles()


if __name__ == "__main__":
    #createDistDir()
    #download(DEFAULT_OSM_FILES[0:1])
    #splitMaps(DEFAULT_OSM_FILES[0:1])
    #fullProcess()
    createMapsFromTiles()
