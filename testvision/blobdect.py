# standard imports
import cv2
import numpy as np;

# Read image
img = cv2.imread("testcases/sudoku01.jpg")
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Set up the detector with default parameters.
detector = cv2.SimpleBlobDetector()

# Detect blobs.
keypoints = detector.detect(gray)

# Draw detected blobs as red circles.
# cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS ensures the size of the circle corresponds to the size of blob
im_with_keypoints = cv2.drawKeypoints(img, keypoints, np.array([]), (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

cv2.imwrite('sudoku01-blobs.png', lines_edges)
import os
os.system('gwenview sudoku01-blobs.png')
