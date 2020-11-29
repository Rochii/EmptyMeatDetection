#!/usr/bin/env python
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

# Base64 operations
import base64

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

# "Constants" (constants in python doesn't exist)
REQUEST_OK = "200"
ERROR_INVALID_METHOD = "1400"
ERROR_INVALID_REQUEST = "1401"
ERROR_INVALID_CONTENT = "1402"
ERROR_NO_DATA = "1403"
ERROR_UNKNOWN = "1500"
ERROR_TRY_AGAIN_LATER = "1507"

# Status code to names
STATUS_TO_NAMES = {
    REQUEST_OK : "Success",
    ERROR_INVALID_METHOD : "Invalid method",
    ERROR_INVALID_REQUEST : "Invalid request",
    ERROR_INVALID_CONTENT : "Invalid content",
    ERROR_NO_DATA : "No data found",
    ERROR_UNKNOWN : "Unknown error",
    ERROR_TRY_AGAIN_LATER : "Service unavailable, try again later",
}

# Accepted ip's
# https://www.geeksforgeeks.org/frozenset-in-python/
ACCEPTED_IPS = frozenset([
    "127.0.0.1", # Localhost
])


# Accepted tokens
AUTHENTICATION_TOKENS = {
    "2b7ef86ff94561072baa6b86323de061" : "apiuser",
}


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


def save_base64img(id, base64img, encoding="iso-8859-1"):
    """Save base64 image into localstore.

    Args:
        id (string): Request id.
        base64img (string): base64 image encoded.
        encoding (string): base64 charset encoding.

    Returns:
        string: image save path.
    """
    imgpath = get_path(id) + "original.jpg"
    with open(imgpath, "wb") as f:
        f.write(base64.b64decode(base64img))

    return imgpath