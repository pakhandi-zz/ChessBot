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
import shutil

# Global Constants
# ---------------------------------------------------------------------------

RED   = (255,0,0)
GREEN = (0,255,0)
BLUE  = (0,0,255)

FACTOR = 8
INT_MAX = 1000000009
TOTAL_FINAL_VERTICES = 150
OFFSET = 30

WHITE_THRESHOLD = 180
BLACK_THRESHOLD = 110

# ---------------------------------------------------------------------------

if len(sys.argv) != 3:
	print "Correct Usage : python chess_board.py <SourceFilename> <NumberOfInitialVertices>"
	exit()

# Reading the image file
img = cv2.imread(sys.argv[1])
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

# Function to get distance between two points in 2-D plane
def get_dist((x1,y1), (x2,y2)):
	return int(sqrt( (y2-y1)**2 + (x2-x1)**2 ))

# Detecting vertices in the image
corners = cv2.goodFeaturesToTrack(gray,int(sys.argv[2]),0.01,10)
corners = np.int0(corners)

vertices = []

# Pushing the detected vertices in the list
for i in corners:
	x,y = i.ravel()
	vertices.append((x,y))
	#cv2.circle(img,(x,y),5,255,-1)
	print x," ",y
print "^"*30
plt.imshow(img),plt.show()

# Variables to store four corners of the board
bottom_left_x = INT_MAX
bottom_left_y = 0

top_left_x = INT_MAX
top_left_y = INT_MAX

bottom_right_x = 0
bottom_right_y = 0

top_right_x = 0
top_right_y = INT_MAX

minny = INT_MAX
maxxy = 0

# Detecting the four corners of the board
# ---------------------------------------------------------------------------

for point in vertices:
	minny = min(point[1],minny)
	maxxy = max(point[1],maxxy)

for point in vertices:
	if(point[1] >= minny - OFFSET and point[1] <= minny + OFFSET):
		print point
		if point[0] > top_right_x:
			top_right_x,top_right_y = point[0],point[1]
		if point[0] < top_left_x:
			top_left_x,top_left_y = point[0],point[1]
	if(point[1] >= maxxy - OFFSET and point[1] <= maxxy + OFFSET):
		print point
		if point[0] > bottom_right_x:
			bottom_right_x,bottom_right_y = point[0],point[1]
		if point[0] < bottom_left_x:
			bottom_left_x,bottom_left_y = point[0],point[1]

# ---------------------------------------------------------------------------

# Marking the four corners of the board
cv2.circle(img,(top_left_x,top_left_y),1,255,-1)
cv2.circle(img,(bottom_left_x,bottom_left_y),1,255,-1)
cv2.circle(img,(bottom_right_x,bottom_right_y),1,255,-1)
cv2.circle(img,(top_right_x,top_right_y),1,255,-1)

# Making four sides around the board
cv2.line(img, (top_left_x,top_left_y), (top_right_x,top_right_y), GREEN, 2)
cv2.line(img, (top_left_x,top_left_y), (bottom_left_x,bottom_left_y), GREEN, 2)
cv2.line(img, (bottom_left_x,bottom_left_y), (bottom_right_x,bottom_right_y), GREEN, 2)
cv2.line(img, (bottom_right_x,bottom_right_y), (top_right_x,top_right_y), GREEN, 2)

plt.imshow(img),plt.show()


# Calculating the points on all the four sides of the boards
# ---------------------------------------------------------------------------
# Top Side

top_line = []
top_line.append( (top_left_x,top_left_y) )
top_line_length = get_dist( (top_left_x, top_left_y) , (top_right_x,top_right_y))
top_unit_length = top_line_length / FACTOR


for i in range(0,FACTOR-1):
	top_line.append( (top_left_x + ( top_unit_length * (i+1) ) , top_left_y ) )

top_line.append( (top_right_x, top_right_y ) )

for point in top_line:
	cv2.circle(img,(point[0],point[1]), 1, BLUE, -1)

# ---------------------------------------------------------------------------
# Bottom Side

bottom_line = []
bottom_line.append( (bottom_left_x,bottom_left_y) )
bottom_line_length = get_dist( (bottom_left_x,bottom_left_y) , (bottom_right_x, bottom_right_y))
bottom_unit_length = bottom_line_length / FACTOR

for i in range(0,FACTOR-1):
	bottom_line.append( (bottom_left_x + ( bottom_unit_length * (i+1) ) , bottom_left_y ) )

bottom_line.append( (bottom_right_x, bottom_right_y) )

for point in bottom_line:
	cv2.circle(img, (int(point[0]),int(point[1])) , 1, BLUE, -1)

# ---------------------------------------------------------------------------
# Left Side

left_line = []
left_line.append( (top_left_x,top_left_y) )
left_line_length = get_dist( (top_left_x,top_left_y) , (bottom_left_x, bottom_left_y))
left_unit_length = left_line_length / FACTOR

for i in range(0,FACTOR-1):
	left_line.append( (top_left_x , top_left_y + ( (i+1) * left_unit_length ) ) );

left_line.append( (bottom_left_x, bottom_left_y) )

for point in left_line:
	cv2.circle(img, (int(point[0]),int(point[1])) , 1, BLUE, -1)

# ---------------------------------------------------------------------------
# Right Side

right_line = []
right_line.append( (top_right_x,top_right_y) )
right_line_length = get_dist( (top_right_x,top_right_y) , (bottom_right_x, bottom_right_y))
right_unit_length = right_line_length / FACTOR

for i in range(0,FACTOR-1):
	right_line.append( (top_right_x , top_right_y + ( (i+1) * right_unit_length ) ) );

right_line.append( (bottom_right_x, bottom_right_y) )

for point in right_line:
	cv2.circle(img, (int(point[0]),int(point[1])) , 1, BLUE, -1)

# ---------------------------------------------------------------------------


# Drawing the remaining edges of the board using the points detected on sides of board
# ---------------------------------------------------------------------------

for i in range(0,FACTOR+1):
	cv2.line(img, (top_line[i][0],top_line[i][1]) , (bottom_line[i][0],bottom_line[i][1]), RED , 1)

for i in range(0,FACTOR+1):
	cv2.line(img, (left_line[i][0],left_line[i][1]) , (right_line[i][0],right_line[i][1]), RED , 1)

# ---------------------------------------------------------------------------

# Detecting vertices on the newly constructed board
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

corners = cv2.goodFeaturesToTrack(gray,int(TOTAL_FINAL_VERTICES),0.01,10)
corners = np.int0(corners)

new_vertices = []

for i in corners:
	x,y = i.ravel()
	new_vertices.append((x,y))

# Matrix to store coordinates of vertices on the board
matrix = [[(0,0) for x in range(FACTOR+2)] for x in range(FACTOR+2)]

topology = [["." for x in range(FACTOR)] for x in range(FACTOR)]

# Filling the matrix
matrix[0][0] = (top_left_x,top_left_y)

for i in range(0,FACTOR+1):
	for j in range(0,FACTOR+1):
		predicted_x = matrix[i][j][0] + top_unit_length
		predicetd_y = matrix[i][j][1] + left_unit_length

		minn_dist = INT_MAX

		for point in new_vertices:
			this_dist = get_dist( point , (predicted_x,matrix[i][j][1])  )
			if this_dist < minn_dist:
				matrix[i][j+1] = point
				minn_dist = this_dist

		minn_dist = INT_MAX

		for point in new_vertices:
			this_dist = get_dist( point , (matrix[i][j][0],predicetd_y)  )
			if this_dist < minn_dist:
				matrix[i+1][j] = point;
				minn_dist = this_dist

# for i in range(0,4):
# 	for j in range(0,4):
# 		print matrix[i][j],
# 	print

# for vertices in new_vertices:
# 	print vertices[0]," ", vertices[1]
# 	cv2.circle(img,(vertices[0],vertices[1]),5,GREEN,-1)

# Marking the vertices on Image
for i in range(0,FACTOR+1):
	for j in range(0,FACTOR+1):
		cv2.circle(img,(matrix[i][j][0],matrix[i][j][1]),3,BLUE,-1)

plt.imshow(img),plt.show()

# Taking out each cell and deciding if :
# 1> it is empty
# 2> it has a black piece
# 3> it has a white piece
for i in range(0,FACTOR):
	for j in range(0,FACTOR):
		cropped = img[matrix[i][j][1]:matrix[i+1][j+1][1] ,matrix[i][j][0]:matrix[i+1][j+1][0]]
		filename = str(i)+str(j)+".jpg"
		c = 0
		white = 0
		black = 0
		for row in cropped:
			for p in row:
				c+=1
				if p[0]<=BLACK_THRESHOLD and p[1]<=BLACK_THRESHOLD and p[2]<=BLACK_THRESHOLD:
					black+=1
				if p[0]>=WHITE_THRESHOLD and p[1]>=WHITE_THRESHOLD and p[2]>=WHITE_THRESHOLD:
					white+=1
		probW = (white*1.0)/(c*1.0)
		probB = (black*1.0)/(c*1.0)

		if(probW > 0.10):
			topology[i][j] = 'W'
		elif probB > 0.10:
			topology[i][j] = 'B'
		cv2.imwrite(filename,cropped)
		shutil.move(filename,"temp/"+filename)

# Printing the final board state
for i in range(0,FACTOR):
	for j in range(0,FACTOR):
		print topology[i][j],
	print ""

plt.imshow(img),plt.show()