#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Created on 2013-05-27

@author : Laurent Stacul
"""

from http.client import HTTPConnection
from urllib.parse import urlparse
import logging
logger = logging.getLogger(__name__)


BUFFER_SIZE = 2048


class DownloadItem(object):

    def __init__(self, resourceUri, dst):
        self.resourceUri = resourceUri
        self.dst = dst
        self.expectedSize = 0
        self.downloadedBytes = 0


class Downloader(object):

    def __init__(self, host, port=80):
        parseResult = urlparse(host)
        self.host = parseResult.hostname
        self.port = port
        self.items = []

    def addItem(self, resourceUri, dst):
        self.items.append(DownloadItem(resourceUri, dst))
        if logger.isEnabledFor(logging.DEBUG):
            logger.debug("Added for download: {} to {}.".format(resourceUri,
                                                                dst))

    def start(self):
        # First a basic sequential implementation
        for item in self.items:
            self.__single(item)

    def __single(self, item):
        """ Downloads a file through HTTP protocol."""
        if logger.isEnabledFor(logging.INFO):
            logger.info("Downloading {}...".format(item.resourceUri))

        conn = HTTPConnection(self.host, self.port, timeout=30)
        if logger.isEnabledFor(logging.DEBUG):
            logger.debug("HTTPConnection created ({}:{})".format(self.host,
                                                                 self.port))
        conn.request("GET", item.resourceUri)
        r = conn.getresponse()
        item.expectedSize = int(r.getheader("Content-Length").split(",")[0])
        try:
            with open(item.dst, 'wb') as f:
                while not r.closed:
                    buf = r.read(BUFFER_SIZE)
                    f.write(buf)
                    item.downloadedBytes += len(buf)
        finally:
            conn.close()
        if logger.isEnabledFor(logging.INFO):
            logger.info("Downloaded {}.".format(item.resourceUri))


if __name__ == "__main__":
    url = "http://download.geofabrik.de/europe/france/alsace-latest.osm.bz2"
    parseresult = urlparse(url)
    host = parseresult.hostname
    port = parseresult.port
    path = parseresult.path
    print(host)
    downloader = Downloader(host, port)
    downloader.addItem(path, "~/alsace.osm.bz2")
    downloader.start()
    print("Done. " + url)
