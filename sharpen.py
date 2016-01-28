'''
	Program to sharpen the input image
'''
import cv2
import numpy as np
import sys
import os
import shutil

#Load source / input image as grayscale, also works on color images...
imgIn = cv2.imread(sys.argv[1], cv2.IMREAD_GRAYSCALE)

#Create the identity filter, but with the 1 shifted to the right!
kernel = np.zeros( (9,9), np.float32)
kernel[4,4] = 2.0   #Identity, times two! 

#Create a box filter:
boxFilter = np.ones( (9,9), np.float32) / 81.0

#Subtract the two:
kernel = kernel - boxFilter

custom = cv2.filter2D(imgIn, -1, kernel)
cv2.imwrite("sharp.jpg", custom)

if not os.path.exists("temp/"):
	os.makedirs("temp/")
shutil.move("sharp.jpg","temp/sharp.jpg")

exit()