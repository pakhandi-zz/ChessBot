'''
	Program to find edges in a given image
'''

import cv2
import numpy as np
from matplotlib import pyplot as plt

img = cv2.imread('img/chess_board_wodden_with_pieces.jpg',0)
edges = cv2.Canny(img,100,200)

plt.subplot(121),plt.imshow(img,cmap = 'gray')
plt.title('Original Image'), plt.xticks([]), plt.yticks([])
plt.subplot(122),plt.imshow(edges,cmap = 'gray')
plt.title('Edge Image'), plt.xticks([]), plt.yticks([])

plt.show()