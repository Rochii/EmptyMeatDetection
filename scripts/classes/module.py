#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__      = "Roger Truchero Visa"
__copyright__   = "Copyright 2020"
__credits__     = []
__license__     = "GPL"
__version__     = "1.0.0"
__maintainer__  = "Roger Truchero Visa"
__email__       = "truchero.roger@gmail.com"
__status__      = "Development"


# Import logger object
#from Logger import Logger

# os operations
import os

# To obtain the line
from inspect import currentframe

# Main path
MAIN_PATH = "/home/local/LLEIDANET/rtruchero/Escritorio/gitprojs/EmptyMeatDetection/"

# Log file
LOG_PATH = MAIN_PATH + "logs/color_detector.log"

# Local store path
STORE_PATH = MAIN_PATH + "localstore/"

# Logger object
#module_logger = Logger(LOG_PATH, "module.py")

def get_lineno():
    """Gets the current call line number.

    Returns:
        integer: line number.
    """
    cf = currentframe()
    return cf.f_back.f_lineno


def get_path(id):
    """Create id image path.

    Args:
        id (string): frame request timestamp.

    Returns:
        string: localstore path for specified id.
    """
    path = STORE_PATH + id + "/"
    if not os.path.exists(path):
        os.mkdir(path)

    return path