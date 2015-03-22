#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
CLI client application.

TODO:
    - progress bar (http://www.linuxtrack.com/t1171-barre-de-progression.htm)
    - parsing arguments

Created on 2013-06-22

@author : Laurent Stacul
"""

import argparse
import re
from abc import ABCMeta, abstractmethod
from datetime import datetime

import scripts.logconfig
scripts.logconfig.configLoggers()
import scripts.mapcreator
import scripts.disttree

_parser = argparse.ArgumentParser()
_parser.add_argument("-i", "--inputmap", type=str,
                     help="The input map descriptor file.",
                     default="map.xml")
_subparsers = _parser.add_subparsers(help="Sub-commands help")

class Command(object, metaclass=ABCMeta):
    """ Base class representing a user command entry."""

    _commands = []

    _command_regex = re.compile(r"^(\w+)Command$")

    @staticmethod
    @abstractmethod
    def register_parser(parser):
        pass

    @classmethod
    def register(cls):
        m = re.match(Command._command_regex, cls.__name__)
        if m:
            cls.name = m.group(1).lower()
        else:
            msg = "Command class name must follow the <name>Command pattern"
            raise Exception(msg)
        Command._commands.append(cls)
        sp = _subparsers.add_parser(cls.name)
        sp.set_defaults(command=cls.name)
        cls.register_parser(sp)

    @staticmethod
    def execute(s, args):
        for c in Command._commands:
            if c.name == s:
                c()(args)

    def __init__(self):
        super().__init__()

    def __call__(self, args):
        start_time = datetime.utcnow()
        print("{} - Running [{}]".format(start_time.isoformat(),
                                         self.name))
        self._do_run(args)
        end_time = datetime.utcnow()
        print("{} - Finished [{}]".format(end_time.isoformat(),
                                          self.name))
        elapsed_time = end_time - start_time
        print("Elapsed time: {}".format(elapsed_time))

    @abstractmethod
    def _do_run(self):
        pass


class AutoRegisterCommand(ABCMeta):

    def __new__(cls, *args, **kwargs):
        newclass = super().__new__(cls, *args, **kwargs)
        newclass.register()
        return newclass


class InitCommand(Command, metaclass=AutoRegisterCommand):

    @staticmethod
    def register_parser(parser):
        parser.help = "Init the working directory"

    def __init__(self):
        super().__init__()

    def _do_run(self, args):
        scripts.disttree.init()


class CleanCommand(Command, metaclass=AutoRegisterCommand):

    @staticmethod
    def register_parser(parser):
        parser.help = "Clean the working directory"

    def __init__(self):
        super().__init__()

    def _do_run(self, args):
        scripts.disttree.clean()


class DownloadCommand(Command, metaclass=AutoRegisterCommand):

    @staticmethod
    def register_parser(parser):
        parser.help = "Download OSM maps."

    def __init__(self):
        super().__init__()

    def _do_run(self, args):
        scripts.disttree.create()
        if scripts.mapcreator.download(args.inputmap) == 0:
            print("Nothing to download")


class SplitCommand(Command, metaclass=AutoRegisterCommand):

    @staticmethod
    def register_parser(parser):
        parser.help = "Split the maps into smaller tiles."

    def __init__(self):
        super().__init__()

    def _do_run(self, args):
        scripts.disttree.create()
        scripts.mapcreator.split_maps()


class BuildCommand(Command, metaclass=AutoRegisterCommand):

    @staticmethod
    def register_parser(parser):
        parser.help = "Build the final gmapsupp file."

    def __init__(self):
        super().__init__()

    def _do_run(self, args):
        scripts.mapcreator.create_map_from_tiles()


def main():
    args = _parser.parse_args()
    Command.execute(args.command, args)


if __name__ == "__main__":
    main()
