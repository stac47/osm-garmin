#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Created on 2013-05-14

@author : Laurent Stacul
"""


class CommandWrapper(object):

    def __init__(self, command, options=[]):
        self.commandLine = [command]
        self.commandLine.extend(options)

    def __str__(self):
        return " ".join(self.commandLine)


class JavaCommandWrapper(CommandWrapper):

    def __init__(self, options=[]):
        super().__init__("java", ["-Xmx1024M"])
        self.commandLine.extend(options)


class MkgmapWrapper(JavaCommandWrapper):

    def __init__(self, jarPath):
        super().__init__(["-jar {}".format(jarPath)])

    def verbose(self):
        self.commandLine.append("--verbose")

    def inputFile(self, s):
        self.commandLine.append("--input-file={}".format(s))

    def gmapsupp(self):
        self.commandLine.append("--gmapsupp")

    def readConfig(self, s):
        self.commandLine.append("--read-config={}".format(s))

    def outputDir(self, s):
        self.commandLine.append("--output-dir={}".format(s))

    def mapName(self, s):
        self.commandLine.append("--mapname=\"{}\"".format(s))

    def description(self, s):
        self.commandLine.append("--description=\"{}\"".format(s))

    def countryName(self, s):
        self.commandLine.append("--country-name=\"{}\"".format(s))

    def countryAbbr(self, abbreviation):
        self.commandLine.append("--country-abbr={}".format(abbreviation))

    def regionName(self, s):
        self.commandLine.append("--region-name=\"{}\"".format(s))

    def regionAbbr(self, abbreviation):
        self.commandLine.append("--region-abbr={}".format(abbreviation))

    def codePage(self, number):
        self.commandLine.append("--code-page={}".format(number))

    def index(self):
        self.commandLine.append("--index")

    def styleFile(self, s):
        self.commandLine.append("--style-file={}".format(s))

    def style(self, s):
        self.commandLine.append("--style={}".format(s))

    def checkStyle(self):
        self.commandLine.append("--check-style")

    def familyId(self, s):
        self.commandLine.append("--family-id={}".format(s))

    def familyName(self, s):
        self.commandLine.append("--family-name=\"{}\"".format(s))

    def productId(self, s):
        self.commandLine.append("--product-id={}".format(s))

    def productVersion(self, s):
        self.commandLine.append("--product-version={}".format(s))

    def seriesName(self, s):
        self.commandLine.append("--series-name=\"{}\"".format(s))

    def copyrightMessage(self, s):
        self.commandLine.append("--copyright-message={}".format(s))

    def licenseFile(self, s):
        self.commandLine.append("--license-file={}".format(s))

    def maxJobs(self, number):
        self.commandLine.append("--max-jobs={}".format(number))

    def route(self):
        self.commandLine.append("--route")

    def removeShortArcs(self, minLength=0):
        self.commandLine.append("--remove-short-arcs={}".format(minLength))

    def generateSea(self, valueList):
        s = ",".join(valueList)
        self.commandLine.append("--generate-sea={}".format(s))

    def tbdfile(self):
        self.commandLine.append("--tbdfile")

    def transparent(self):
        self.commandLine.append("--transparent")

    def poiAddress(self):
        self.commandLine.append("--poi-address")
