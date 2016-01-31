'''
	Program to find vertices in an image
'''

import numpy as np
import cv2
import sys
from matplotlib import pyplot as plt

img = cv2.imread(sys.argv[1])
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

corners = cv2.goodFeaturesToTrack(gray,int(sys.argv[2]),0.01,10)
corners = np.int0(corners)

ls = []

for i in corners:
	x,y = i.ravel()
	ls.append((x,y))
	#print x," ",y
	#cv2.circle(img,(x,y),3,255,-1)

b_l_x = 10000
b_l_y = 0

t_l_x = 10000
t_l_y = 10000

b_r_x = 0
b_r_y = 0

t_r_x = 0
t_r_y = 10000

minnx = 10000007

for point in ls:
	if point[0] <= t_l_x and point[1] <= t_l_y:
		t_l_x,t_l_y = point[0],point[1]
	if point[0] <= b_l_x and point[1] >= b_l_y:
		b_l_x,b_l_y = point[0],point[1]
	if point[0] >= b_r_x and point[1] >= b_r_y:
		b_r_x,b_r_y = point[0],point[1]
	if point[0] >= t_r_x and point[1] <= t_r_y:
		print point[0]," ",point[1]
		t_r_x,t_r_y = point[0],point[1]



cv2.circle(img,(t_l_x,t_l_y),3,255,-1)
cv2.circle(img,(b_l_x,b_l_y),3,255,-1)
cv2.circle(img,(b_r_x,b_r_y),3,255,-1)
cv2.circle(img,(t_r_x,t_r_y),3,255,-1)

#print tx," ",ty
#	print point[0]," ",point[1]

plt.imshow(img),plt.show()