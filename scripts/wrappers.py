#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Created on 2013-05-14

@author : Laurent Stacul
"""


class CommandWrapper(object):

    def __init__(self, command, options=[]):
        self.command_line = [command]
        self.command_line.extend(options)

    def __str__(self):
        return " ".join(self.command_line)


class JavaCommandWrapper(CommandWrapper):

    def __init__(self, options=[]):
        super().__init__("java", ["-Xmx1024M"])
        self.command_line.extend(options)


class MkgmapWrapper(JavaCommandWrapper):

    def __init__(self, jar_path):
        super().__init__(["-jar {}".format(jar_path)])

    def verbose(self):
        self.command_line.append("--verbose")

    def input_file(self, s):
        self.command_line.append("--input-file={}".format(s))

    def gmapsupp(self):
        self.command_line.append("--gmapsupp")

    def read_config(self, s):
        self.command_line.append("--read-config={}".format(s))

    def output_dir(self, s):
        self.command_line.append("--output-dir={}".format(s))

    def map_name(self, s):
        self.command_line.append("--mapname=\"{}\"".format(s))

    def description(self, s):
        self.command_line.append("--description=\"{}\"".format(s))

    def country_name(self, s):
        self.command_line.append("--country-name=\"{}\"".format(s))

    def country_abbr(self, abbreviation):
        self.command_line.append("--country-abbr={}".format(abbreviation))

    def region_name(self, s):
        self.command_line.append("--region-name=\"{}\"".format(s))

    def region_abbr(self, abbreviation):
        self.command_line.append("--region-abbr={}".format(abbreviation))

    def code_page(self, number):
        self.command_line.append("--code-page={}".format(number))

    def index(self):
        self.command_line.append("--index")

    def style_file(self, s):
        self.command_line.append("--style-file={}".format(s))

    def style(self, s):
        self.command_line.append("--style={}".format(s))

    def check_style(self):
        self.command_line.append("--check-style")

    def family_id(self, s):
        self.command_line.append("--family-id={}".format(s))

    def family_name(self, s):
        self.command_line.append("--family-name=\"{}\"".format(s))

    def product_id(self, s):
        self.command_line.append("--product-id={}".format(s))

    def product_version(self, s):
        self.command_line.append("--product-version={}".format(s))

    def series_name(self, s):
        self.command_line.append("--series-name=\"{}\"".format(s))

    def copyright_message(self, s):
        self.command_line.append("--copyright-message={}".format(s))

    def license_file(self, s):
        self.command_line.append("--license-file={}".format(s))

    def max_jobs(self, number):
        self.command_line.append("--max-jobs={}".format(number))

    def route(self):
        self.command_line.append("--route")

    def remove_short_arcs(self, min_length=0):
        self.command_line.append("--remove-short-arcs={}".format(min_length))

    def generate_sea(self, value_list):
        s = ",".join(value_list)
        self.command_line.append("--generate-sea={}".format(s))

    def tbdfile(self):
        self.command_line.append("--tbdfile")

    def transparent(self):
        self.command_line.append("--transparent")

    def poi_address(self):
        self.command_line.append("--poi-address")
