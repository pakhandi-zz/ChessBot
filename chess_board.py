'''
	Program to:
	1> Detect the chess-board
	2> Make the edges
	3> Device a method to address each cell on the board
'''

import numpy as np
import cv2
import sys
from matplotlib import pyplot as plt
from math import *
import Image, ImageDraw

RED   = (255,0,0)
GREEN = (0,255,0)
BLUE  = (0,0,255)

#Function to get distance between two points in 2-D plane
def get_dist((x1,y1), (x2,y2)):
	return int(sqrt( (y2-y1)**2 + (x2-x1)**2 ))

#Reading the image file
img = cv2.imread(sys.argv[1])
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

corners = cv2.goodFeaturesToTrack(gray,int(sys.argv[2]),0.01,10)
corners = np.int0(corners)

vertices = []

#Pushing the detected vertices in the list
for i in corners:
	x,y = i.ravel()
	vertices.append((x,y))

#Variables to store four corners of the board
b_l_x = 10000
b_l_y = 0

t_l_x = 10000
t_l_y = 10000

b_r_x = 0
b_r_y = 0

t_r_x = 0
t_r_y = 10000

minnx = 10000007

#Detecting the four corners of the board
for point in vertices:
	if point[0] <= t_l_x and point[1] <= t_l_y:
		t_l_x,t_l_y = point[0],point[1]
	if point[0] <= b_l_x and point[1] >= b_l_y:
		b_l_x,b_l_y = point[0],point[1]
	if point[0] >= b_r_x and point[1] >= b_r_y:
		b_r_x,b_r_y = point[0],point[1]
	if point[0] >= t_r_x and point[1] <= t_r_y:
		print point[0]," ",point[1]
		t_r_x,t_r_y = point[0],point[1]

#Marking the four corners of the board
cv2.circle(img,(t_l_x,t_l_y),1,255,-1)
cv2.circle(img,(b_l_x,b_l_y),1,255,-1)
cv2.circle(img,(b_r_x,b_r_y),1,255,-1)
cv2.circle(img,(t_r_x,t_r_y),1,255,-1)

#Making four sides around the board
cv2.line(img, (t_l_x,t_l_y), (t_r_x,t_r_y), GREEN, 2)
cv2.line(img, (t_l_x,t_l_y), (b_l_x,b_l_y), GREEN, 2)
cv2.line(img, (b_l_x,b_l_y), (b_r_x,b_r_y), GREEN, 2)
cv2.line(img, (b_r_x,b_r_y), (t_r_x,t_r_y), GREEN, 2)

#Calculating the points on all the four sides of the boards
# ------------TOP Side------------------------

top_line = []
top_line.append( (t_l_x,t_l_y) )
top_line_length = get_dist( (t_l_x, t_l_y) , (t_r_x,t_r_y))
top_unit_length = top_line_length / 3


for i in range(0,2):
	top_line.append( (t_l_x + ( top_unit_length * (i+1) ) , t_l_y ) )

top_line.append( (t_r_x, t_r_y ) )

for point in top_line:
	cv2.circle(img,(point[0],point[1]), 1, BLUE, -1)

# -------------BOTTOM Side---------------------------------------

bottom_line = []
bottom_line.append( (b_l_x,b_l_y) )
bottom_line_length = get_dist( (b_l_x,b_l_y) , (b_r_x, b_r_y))
bottom_unit_length = bottom_line_length / 3

for i in range(0,2):
	bottom_line.append( (b_l_x + ( bottom_unit_length * (i+1) ) , b_l_y ) )

bottom_line.append( (b_r_x, b_r_y) )

for point in bottom_line:
	cv2.circle(img, (int(point[0]),int(point[1])) , 1, BLUE, -1)

# -------------LEFT Side--------------------------------------------

left_line = []
left_line.append( (t_l_x,t_l_y) )
left_line_length = get_dist( (t_l_x,t_l_y) , (b_l_x, b_l_y))
left_unit_length = left_line_length / 3

for i in range(0,2):
	left_line.append( (t_l_x , t_l_y + ( (i+1) * left_unit_length ) ) );

left_line.append( (b_l_x, b_l_y) )

for point in left_line:
	cv2.circle(img, (int(point[0]),int(point[1])) , 1, BLUE, -1)

# -------------RIGHT Side----------------------------------------------

right_line = []
right_line.append( (t_r_x,t_r_y) )
right_line_length = get_dist( (t_r_x,t_r_y) , (b_r_x, b_r_y))
right_unit_length = right_line_length / 3

for i in range(0,2):
	right_line.append( (t_r_x , t_r_y + ( (i+1) * right_unit_length ) ) );

right_line.append( (b_r_x, b_r_y) )

for point in right_line:
	cv2.circle(img, (int(point[0]),int(point[1])) , 1, BLUE, -1)

# --------------------------------------------------------------------------------


#Drawing the remaining edges of the board using the points detected on sides of board
# --------------------------------------------------------------------------------

for i in range(0,4):
	cv2.line(img, (top_line[i][0],top_line[i][1]) , (bottom_line[i][0],bottom_line[i][1]), RED , 1)

for i in range(0,4):
	cv2.line(img, (left_line[i][0],left_line[i][1]) , (right_line[i][0],right_line[i][1]), RED , 1)

# -------------------------------------------------------------------------------

#Detecting vertices on the newly constructed board
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

corners = cv2.goodFeaturesToTrack(gray,int(16),0.01,10)
corners = np.int0(corners)

new_vertices = []

for i in corners:
	x,y = i.ravel()
	new_vertices.append((x,y))

#Matrix to store coordinates of vertices on the board
matrix = [[(0,0) for x in range(5)] for x in range(5)]

#Filling the matrix
matrix[0][0] = (t_l_x,t_l_y)

for i in range(0,4):
	for j in range(0,4):
		predicted_x = matrix[i][j][0] + top_unit_length
		predicetd_y = matrix[i][j][1] + left_unit_length

		minn_dist = 1000000009

		for point in new_vertices:
			this_dist = get_dist( point , (predicted_x,matrix[i][j][1])  )
			if this_dist < minn_dist:
				matrix[i][j+1] = point
				minn_dist = this_dist

		minn_dist = 1000000009

		for point in new_vertices:
			this_dist = get_dist( point , (matrix[i][j][0],predicetd_y)  )
			if this_dist < minn_dist:
				matrix[i+1][j] = point;
				minn_dist = this_dist

# for i in range(0,4):
# 	for j in range(0,4):
# 		print matrix[i][j],
# 	print

for vertices in new_vertices:
	print vertices[0]," ", vertices[1]
	cv2.circle(img,(vertices[0],vertices[1]),5,GREEN,-1)

plt.imshow(img),plt.show()