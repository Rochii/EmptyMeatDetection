#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__      = "Roger Truchero Visa"
__copyright__   = "Copyright 2020"
__credits__     = []
__license__     = "GPL"
__version__     = "1.0.0"
__maintainer__  = "Roger Truchero Visa"
__email__       = "truchero.roger@lleida.net"
__status__      = "Development"


from module import LOG_PATH, get_lineno, get_path
from Logger import Logger

import cv2
import numpy as np
import sys
import time


class ColorDetector():

    def __init__(self):
        """Initialize object.
        """
        self.logger = Logger(LOG_PATH, "ColorDetector.py")
        self.logger.info(":__init__ info: Initializing logger object", get_lineno())
        self.colors = {
            # BGR
            "blue" : ([50, 0, 0], [255, 50, 50]),
            "green" : ([0, 50, 0], [50, 255, 50]),
            "red" : ([0, 0, 50], [50, 50, 255])
        }


    def identify_color_areas(self, image_path, color="green"):
        """Identify regions between lower and upper color intervals.
        Estimate the empty area using the color.
        Based on this value send fill alarm.
        The image also shows the capture with the empty areas within a rectangle.

        Args:
            image_path (string): Image path.
            color (string, optional): Color to detect. Defaults to "green".

        Returns:
            string: the saved image path if all ok, empty string otherwise.
        """
        if color not in self.colors:
            self.logger.error(":identify_area color: {0} error: Invalid color!".format(color), get_lineno())
            return ""

        lower, upper = np.array(self.colors[color], dtype="uint8") # Obtain corresponding lower and upper color values
        image = cv2.imread(image_path) # Read image
        mask = cv2.inRange(image, lower, upper) # Find the color specified and apply the mask
        output = cv2.bitwise_and(image, image, mask=mask)
        save_path = self.save_dir + image_path.split("/")[-1] # Define save path
        cv2.imwrite(save_path, output) # Save image

        return save_path


    def identify_color_contours(self, image_path, color="green"):
        """Identify regions between lower and upper color intervals.
        Estimate the empty area using the color.
        Based on this value send fill alarm.
        The image also shows the capture with the empty areas within a rectangle.

        Args:
            image_path (string): Image path.
            color (string, optional): Color to detect. Defaults to "green".

        Returns:
            string: the timestamp id if images saved OK, empty string otherwise.
        """
        id = str(int(time.time())) # Obtain id
        self.logger.error(":identify_color_contours id:{0} color: {1}".format(id, color), get_lineno())

        if color not in self.colors:
            self.logger.error(":identify_color_contours id: {0} color: {1} error: Invalid color!".format(id, color), get_lineno())
            return ""

        lower, upper = np.array(self.colors[color], dtype="uint8") # Obtain corresponding lower and upper color values
        image = cv2.imread(image_path) # Read image
        #hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV) # Convert BGR to HSV
        mask = cv2.inRange(image, lower, upper) # Find the color specified and apply the mask
        contours = cv2.findContours(mask.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)[-2]

        if len(contours) > 0:
            #red_area = max(contours, key=cv2.contourArea)
            for contour in contours:
                x, y, w, h = cv2.boundingRect(contour)
                cv2.rectangle(image, (x, y),(x+w, y+h), (0, 0, 255), 2)

            # Make request directory
            ext = image_path.split(".")[-1]
            path = get_path(id)
            save_image_path = path + "frame." + ext
            save_mask_path = path + "mask." + ext
            self.logger.info(":identify_color_contours id: {0} ext: {1} save_image_path: {2} save_mask_path: {3}".format(id, ext, save_image_path, save_mask_path), get_lineno())

            cv2.imwrite(save_image_path, image) # Save image with rectangle areas
            self.logger.info(":identify_color_contours id: {0} save_image_path: {1} info: Image saved OK!".format(id,save_mask_path), get_lineno())

            cv2.imwrite(save_mask_path, mask) # Save image mask
            self.logger.info(":identify_color_contours id: {0} save_mask_path: {1} info: Mask saved OK!".format(id, save_mask_path), get_lineno())

            return id

        self.logger.info(":identify_color_contours image_path: {0} color: {1} len(contours): {2} info: empty contours".format(image_path, color, len(contours)), get_lineno())
        return ""


if __name__ == "__main__":
    if len(sys.argv) == 2:
        detector = ColorDetector()
        id = detector.identify_color_contours(sys.argv[1])
    else:
        print("Usage: python main.py <image_path>")