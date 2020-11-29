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

        # Coordinates coefficients
        self.B_COEFF = 0.6481
        self.C_COEFF = 0.5338
        self.D_COEFF_W = self.C_COEFF
        self.D_COEFF_H = 0.3981
        self.F_COEFF = 0.2344


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
        self.logger.info(":identify_color_contours id:{0} color: {1}".format(id, color), get_lineno())

        if color not in self.colors:
            self.logger.error(":identify_color_contours id: {0} color: {1} error: Invalid color!".format(id, color), get_lineno())
            return ""

        lower, upper = np.array(self.colors[color], dtype="uint8") # Obtain corresponding lower and upper color values
        image = cv2.imread(image_path) # Read image
        self.HEIGHT, self.WIDTH, _ = image.shape # Obtain height and widht sizes
        self.logger.info(":identify_color_contours id: {0} height: {1} width: {2}".format(id, self.HEIGHT, self.WIDTH), get_lineno())

        mask = cv2.inRange(image, lower, upper) # Find the color specified and apply the mask
        contours = cv2.findContours(mask.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)[-2] # Find all contours

        empty_holes = 0

        if len(contours) > 0:
            #red_area = max(contours, key=cv2.contourArea)
            for contour in contours:
                x, y, w, h = cv2.boundingRect(contour)
                contour_area = cv2.contourArea(contour)
                if self.is_valid_contour(contour_area, x, y, w, h):
                    cv2.rectangle(image, (x, y), (x+w, y+h), (0, 0, 255), 2)
                    empty_holes += 1
                    #cv2.drawContours(image, contour, -1, (0, 0, 255), 2)
                    self.logger.info(":identify_color_contours id: {0} contour_area: {1} empty_holes: {2} values: {3}".format(id, contour_area, empty_holes, (x, y, w, h)), get_lineno())

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


    def print_triangle_lines(self, image):
        """Print triangle lines in the canvas.

        Args:
            image (object): cv2 image object.

        Returns:
            object: Modified image canvas object with lines addition.
        """
        A = (0, 0)
        B = tuple(map(int, (0, self.HEIGHT*self.B_COEFF)))
        C = tuple(map(int, (self.WIDTH*self.C_COEFF, 0)))
        D = tuple(map(int, (self.WIDTH*self.D_COEFF_W, self.HEIGHT*self.D_COEFF_H)))
        E = tuple(map(int, (self.WIDTH*self.C_COEFF, self.HEIGHT)))
        F = tuple(map(int, (self.WIDTH*self.F_COEFF, self.HEIGHT)))

        cv2.line(image, A, B, (0, 0, 255), 3) # Segment AB
        cv2.line(image, B, C, (0, 0, 255), 3) # Segment BC
        cv2.line(image, C, A, (0, 0, 255), 3) # Segment CA
        cv2.line(image, D, E, (0, 0, 255), 3) # Segment DE
        cv2.line(image, E, F, (0, 0, 255), 3) # Segment EF
        cv2.line(image, F, D, (0, 0, 255), 3) # Segment FD
        cv2.line(image, C, D, (0, 255, 0), 3) # Segment CD

        return image


    def is_valid_contour(self, contour_area, x, y, w, h):
        """Check if contour is valid.

        Args:
            contour_area (float): effective colored area.
            x (int): top-left rectangle x coordinate.
            y (int): top-left rectangle y coordinate.
            w (int): rectangle width.
            h (int): rectangle height.

        Returns:
            boolean: True if point is within the valid area, False otherwise.
        """
        # Compute the ponderate point coordinates
        A = (0, 0)
        B = tuple(map(int, (0, self.HEIGHT*self.B_COEFF)))
        C = tuple(map(int, (self.WIDTH*self.C_COEFF, 0)))
        D = tuple(map(int, (self.WIDTH*self.D_COEFF_W, self.HEIGHT*self.D_COEFF_H)))
        E = tuple(map(int, (self.WIDTH*self.C_COEFF, self.HEIGHT)))
        F = tuple(map(int, (self.WIDTH*self.F_COEFF, self.HEIGHT)))
        P = (x+w, y+h)
        #self.logger.info(":is_valid_contour contour_area: {0} A: {1} B: {2} C: {3} D: {4} E: {5} F: {6} P: {7}".format(contour_area, A, B, C, D, E, F, P), get_lineno())

        """
            We only are interested in x parts so, we exclude the following vectorial points:
                * Points within ABC triangle
                * Points within DEF triangle
                * Points at the right of C
                * Points with an effective are greater than 300

            A___________________C_______________________
            |                xxxx                      |
            |             xxxxxxx                      |
            |        xxxxxxxxxxxD                      |
            |     xxxxxxxxxxxx                         |
            Bxxxxxxxxxxxxxx                            |
            |xxxxxxxxxxxx                              |
            |xxxxxxxxx                                 |
            |xxxxxxxF___________E______________________|
        """

        return not self.is_inside(A[0], A[1], B[0], B[1], C[0], C[1], P[0], P[1]) and not self.is_inside(D[0], D[1], E[0], E[1], F[0], F[1], P[0], P[1]) and x+w <= C[0] and contour_area >= 300


    # A utility function to calculate area of triangle formed by (x1, y1), (x2, y2) and (x3, y3)
    def area(self, x1, y1, x2, y2, x3, y3):
        """Calculates the are of a triangle using their vectorials coordinates.

        Args:
            x1 (int): vertex A.x triangle coordinate.
            y1 (int): vertex A.y triangle coordinate.
            x2 (int): vertex B.x triangle coordinate.
            y2 (int): vertex B.y triangle coordinate.
            x3 (int): vertex C.x triangle coordinate.
            y3 (int): vertex C.y triangle coordinate.

        Returns:
            float: triangle area value.
        """
        return abs((x1 * (y2 - y3) + x2 * (y3 - y1) + x3 * (y1 - y2)) / 2.0)


    # A function to check whether point P(x, y) lies inside the triangle formed by A(x1, y1), B(x2, y2) and C(x3, y3)
    def is_inside(self, x1, y1, x2, y2, x3, y3, x, y):
        """Check if a P(x, y) coordinate is inside ABC triangle.

        Args:
            x1 (int): vertex A.x triangle coordinate.
            y1 (int): vertex A.y triangle coordinate.
            x2 (int): vertex B.x triangle coordinate.
            y2 (int): vertex B.y triangle coordinate.
            x3 (int): vertex C.x triangle coordinate.
            y3 (int): vertex C.y triangle coordinate.
            x (int): vertex P.x triangle coordinate.
            y (int): vertex P.y triangle coordinate.

        Returns:
            boolean: True if the coordinate P(x, y) is inside the ABC triangle, False otherwise.
        """
        # Calculate area of triangle ABC
        A = self.area(x1, y1, x2, y2, x3, y3)

        # Calculate area of triangle PBC
        A1 = self.area(x, y, x2, y2, x3, y3)

        # Calculate area of triangle PAC
        A2 = self.area(x1, y1, x, y, x3, y3)

        # Calculate area of triangle PAB
        A3 = self.area(x1, y1, x2, y2, x, y)

        # Check if sum of A1, A2 and A3 is same as A
        return True if A == A1 + A2 + A3 else False



if __name__ == "__main__":
    if len(sys.argv) == 2:
        detector = ColorDetector()
        id = detector.identify_color_contours(sys.argv[1])
    else:
        print("Usage: python main.py <image_path>")