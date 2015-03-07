#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Created on 2013-05-27

@author : Laurent Stacul
"""

from http.client import HTTPConnection
from urllib.parse import urlparse
import multiprocessing as mp
import logging
logger = logging.getLogger(__name__)


BUFFER_SIZE = 2048


class DownloadItem(object):

    def __init__(self, resource_uri, dst):
        self.resource_uri = resource_uri
        self.dst = dst
        self.expected_size = 0
        self.downloaded_bytes = 0


class Downloader(object):

    def __init__(self, host, port=80):
        parse_result = urlparse(host)
        self.host = parse_result.hostname
        self.port = port
        self.items = []
        if logger.isEnabledFor(logging.DEBUG):
            logger.debug("Ready to download from: {}:{}".format(self.host,
                                                                self.port))

    def add_item(self, resource_uri, dst):
        self.items.append(DownloadItem(resource_uri, dst))
        if logger.isEnabledFor(logging.DEBUG):
            logger.debug("Added for download: {} to {}.".format(resource_uri,
                                                                dst))

    def start(self):
        pool = mp.Pool(processes=4)
        pool.map(self.single, self.items)

    def single(self, item):
        """ Downloads a file through HTTP protocol."""
        if logger.isEnabledFor(logging.INFO):
            logger.info("Downloading {}...".format(item.resource_uri))

        conn = HTTPConnection(self.host, self.port, timeout=30)
        if logger.isEnabledFor(logging.DEBUG):
            logger.debug("HTTPConnection created ({}:{})".format(self.host,
                                                                 self.port))
        conn.request("GET", item.resource_uri)
        r = conn.getresponse()
        item.expected_size = int(r.getheader("Content-Length").split(",")[0])
        try:
            with open(item.dst, 'wb') as f:
                while item.downloaded_bytes < item.expected_size:
                    buf = r.read(BUFFER_SIZE)
                    f.write(buf)
                    item.downloaded_bytes += len(buf)
                    if item.downloaded_bytes % (BUFFER_SIZE * 25) == 0 \
                            and logger.isEnabledFor(logging.DEBUG):
                        msg = "Downloaded: {}/{}"
                        logger.debug(msg.format(item.downloaded_bytes,
                                                item.expected_size))
        finally:
            conn.close()
        if logger.isEnabledFor(logging.INFO):
            logger.info("Downloaded {}.".format(item.resource_uri))


if __name__ == "__main__":
    urls = [
        "http://download.geofabrik.de/europe/france/alsace-latest.osm.bz2",
        "http://download.geofabrik.de/europe/france/aquitaine-latest.osm.bz2"
    ]
    downloader = None
    for url in urls:
        parse_result = urlparse(url)
        if downloader is None:
            host = parse_result.hostname
            port = parse_result.port
            downloader = Downloader(host, port)
        path = parse_result.path
        downloader.add_item(path, "~/alsace.osm.bz2")
    downloader.start()
    print("Done. " + url)
