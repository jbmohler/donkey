import os
import datetime
import cv2
import numpy as np

print(datetime.datetime.now())

filename = 'sudoku01.jpg'
img = cv2.imread(filename)
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

gray = np.float32(gray)
dst = cv2.cornerHarris(gray,25,3,0.04)

#result is dilated for marking the corners, not important
dst = cv2.dilate(dst,None)

# Threshold for an optimal value, it may vary depending on the image.
img[dst>0.05*dst.max()]=[0,0,255]

print(dst.shape)

cv2.imwrite('sudoku01-corners.png', img)
os.system('xdg-open sudoku01-corners.png')
#cv2.imshow('dst',img)
#if cv2.waitKey(0) & 0xff == 27:
#    cv2.destroyAllWindows()
