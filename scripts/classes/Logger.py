#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__      = "Roger Truchero Visa"
__copyright__   = "Copyright 2020"
__credits__     = []
__license__     = "GPL"
__version__     = "1.0.0"
__maintainer__  = "Roger Truchero Visa"
__email__       = "rtruchero@lleida.net"
__status__      = "Development"


import logging
import time
import uuid


class Logger():
    """Generic class to do log.
    The defined levels, in order of increasignly severity, are the following:
        - debug: Detailed information, typically of interest only when diagnosing problems.
        - info: Confirmation that things are working as expected.
        - warning: An indication that something unexpected happened, or indicative of some problem in the near future (e.g. ‘disk space low’). The software is still working as expected.
        - error: Due to a more serious problem, the software has not been able to perform some function.
        - critical: A serious error, indicating that the program itself may be unable to continue running.
    """

    def __init__(self, logpath, name, level=logging.INFO):
        """Initialize Logger object.

        Args:
            logpath (string): Log path file.
            name (string) : Class that instantiates the current Logger object.
            level (object, optional): Sets the logging level. Defaults to logging.INFO.
        """
        # get logger for 'name'
        self.logger = logging.getLogger(name)

        # define format
        formatter = logging.Formatter('%(asctime)s,%(msecs)d %(levelname)s {0} {1}:%(message)s'.format(uuid.uuid4().hex, name))

        # define the file handler to the specified logpath
        file_handler = logging.FileHandler(logpath)
        file_handler.setFormatter(formatter)

        # set the logging level and add the file handler
        self.logger.setLevel(level)
        self.logger.addHandler(file_handler)


    def debug(self, msg, line):
        """Debug function.

        Args:
            msg (string): message to log.
            line (integer): log corresponding line of file.
        """
        self.logger.debug("{0} time:{1} {2}".format(line, int(time.time()), msg))


    def info(self, msg, line):
        """Info function.

        Args:
            msg (string): message to log.
            line (integer): log corresponding line of file.
        """
        self.logger.info("{0} time:{1} {2}".format(line, int(time.time()), msg))


    def warning(self, msg, line):
        """Warning function.

        Args:
            msg (string): message to log.
            line (integer): log corresponding line of file.
        """
        self.logger.warning("{0} time:{1} {2}".format(line, int(time.time()), msg))


    def error(self, msg, line):
        """Error function.

        Args:
            msg (string): message to log.
            line (integer): log corresponding line of file.
        """
        self.logger.error("{0} time:{1} {2}".format(line, int(time.time()), msg))


    def critical(self, msg, line):
        """Critical function.

        Args:
            msg (string): message to log.
            line (integer): log corresponding line of file.
        """
        self.logger.critical("{0} time:{1} {2}".format(line, int(time.time()), msg))