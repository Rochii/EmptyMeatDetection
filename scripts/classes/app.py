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


# Flask imports
from flask import Flask, request, jsonify
from flask_httpauth import HTTPTokenAuth

# Module imports
from Logger import Logger
from ColorDetector import ColorDetector
from module import *
import time


app = Flask(__name__) # Initialize Flask app
auth = HTTPTokenAuth(scheme='Bearer') # Initialize bearer authentication token
logger = Logger(LOG_PATH, "app.py") # Logger object
detector = ColorDetector() # ColorDetector object

@auth.verify_token
def verify_token(token):
    """Verify that 'token' is valid.

    Args:
        token (string): bearer authenticatin token.

    Returns:
        string: user corresponding token.
    """
    if token in AUTHENTICATION_TOKENS:
        return AUTHENTICATION_TOKENS[token]


@app.route("/detect", methods=["POST"])
@auth.login_required
def detect():
    """Detect API POST method.
    Validate ip and body. If information is valid generate id and detect empty holes.
    If OK, returns a json response with the code, status, id, empty_holes and base64 image.
    Otherwise returns a json response with the code, status and the remote ip address.

    Returns:
       flask.wrappers.Response: represents the response json object to return.
    """

    user = auth.current_user()

    # Validate ip
    remote_addr = request.remote_addr
    logger.info(":detect user: {0} remote_addr: {1}".format(user, remote_addr), get_lineno())
    if not validate_ip(remote_addr):
        logger.warning(":detect user: user: {0} remote_addr: {1} error: invalid remote ip!".format(user, remote_addr), get_lineno())
        return get_json_response(ERROR_INVALID_REQUEST, STATUS_TO_NAMES[ERROR_INVALID_REQUEST], remote_addr)

    # Validate json body
    # Check if the mimetype indicates JSON data, either application/json or application/*+json
    if request.is_json:
        try:
            # Parse data as JSON
            content = request.get_json()

            # Search for "frame" request parameter
            if "frame" not in content:
                logger.error(":detect user: {0} remote_addr: {1} content: {2} error: frame field not found!".format(user, remote_addr, content), get_lineno())
                return get_json_response(ERROR_INVALID_REQUEST, STATUS_TO_NAMES[ERROR_INVALID_REQUEST], remote_addr)

            # Obtain timestamp id and path
            id = str(int(time.time()))

            # Check if image is base64 and save it, save function returns the path
            base64img = save_base64img(id, content["frame"])
            logger.info(":detect user: {0} info: saved base64 img successful!".format(user), get_lineno())

            # Call identify_color_contours method
            response = detector.identify_color_contours(id, base64img)

            return get_json_response(REQUEST_OK, STATUS_TO_NAMES[REQUEST_OK], remote_addr, id, response)

        except Exception as e:
            logger.error(":detect user: {0} remote_addr: {1} e: {2} error: invalid json content!".format(user, remote_addr, e), get_lineno())
            return get_json_response(ERROR_INVALID_CONTENT, STATUS_TO_NAMES[ERROR_INVALID_CONTENT], remote_addr)
    else:
        logger.error(":detect user: {0} remote_addr: {1} error: non json request!".format(user, remote_addr), get_lineno())
        return get_json_response(ERROR_INVALID_REQUEST, STATUS_TO_NAMES[ERROR_INVALID_REQUEST], remote_addr)


def validate_ip(ip):
    """Validate source ip.

    Args:
        ip (string): remote host ip.

    Returns:
        boolean: returns True if ip is accepted, False otherwise.
    """
    return ip in ACCEPTED_IPS


def get_json_response(code, status, remote_addr, id=None, attributes=None):
    """"Generic json response function.

    Args:
        code (string): status code.
        status (string): status description.
        remote_addr (string): remote source ip address.
        id (string, optional): petition id. Default to None.
        attributes (dictionary, optional): dictionary containing response attributes. Default to None.

    Returns:
        flask.wrappers.Response: represents the response json object to return.
    """

    response = ({ "code" : code, "status" : status })

    # Add id if we have it
    if id != None:
        response["id"] = id
        logger.info(":get_json id: {0} info: added id to response".format(id), get_lineno())

    # Add attributes if we have it
    if attributes != None:
        response["attributes"] = attributes
        logger.info(":get_json attributes: {0} info: added attributes to response".format(attributes), get_lineno())

    # If request NOOK, add the remote_addr
    if code != REQUEST_OK:
        response["remote_addr"] = remote_addr
        logger.info(":get_json remote_addr: {0} info: request code NOOK, added remote_addr to response".format(remote_addr), get_lineno())

    logger.info(":get_json_response response: {0}".format(response), get_lineno())

    return jsonify(response)


if __name__ == "__main__":
    app.run(debug=True, host="localhost")