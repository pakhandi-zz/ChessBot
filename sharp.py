import cv2
import numpy as np
import sys

#Linux window/threading setup code.
cv2.startWindowThread()
cv2.namedWindow("Original")
cv2.namedWindow("Sharpen")

#Load source / input image as grayscale, also works on color images...
imgIn = cv2.imread(sys.argv[1], cv2.IMREAD_GRAYSCALE)
cv2.imshow("Original", imgIn)


#Create the identity filter, but with the 1 shifted to the right!
kernel = np.zeros( (9,9), np.float32)
kernel[4,4] = 2.0   #Identity, times two! 

#Create a box filter:
boxFilter = np.ones( (9,9), np.float32) / 81.0

#Subtract the two:
kernel = kernel - boxFilter

custom = cv2.filter2D(imgIn, -1, kernel)
cv2.imshow("Sharpen", custom)

cv2.imwrite("sharp.jpg", custom)

cv2.destroyAllWindows()
exit()