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


import cv2
import numpy as np
import sys

class EmptyDetector():

    def __init__(self):
        self.save_dir = "/home/local/LLEIDANET/rtruchero/Escritorio/gitprojs/EmptyMeatDetection/images/outs/"


    def identify_green_areas(self, image_path):
        # Read image
        image = cv2.imread(image_path)

        # Create NumPy arrays from the boundaries
        # ... BGR
        lower = np.array([0, 50, 0], dtype = "uint8")
        upper = np.array([50, 255, 50], dtype = "uint8")

        # Find the colors within the specified boundaries and apply the mask
        mask = cv2.inRange(image, lower, upper)
        output = cv2.bitwise_and(image, image, mask=mask)

        # Save image
        cv2.imwrite(self.save_dir + image_path.split("/")[-1], output)

        # Show the images
        #cv2.imshow("images", np.hstack([image, output]))
        #cv2.waitKey(0)


if __name__ == "__main__":
    if len(sys.argv) == 2:
        detector = EmptyDetector()
        detector.identify_green_areas(sys.argv[1])
    else:
        print("Usage: python main.py <image_path>")