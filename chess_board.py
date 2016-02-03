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
OFFSET = 10

WHITE_THRESHOLD = 142
BLACK_THRESHOLD = 80

PROBABILITY_THRESHOLD = 0.13

# ---------------------------------------------------------------------------

# Checking arguments
if len(sys.argv) != 3:
	print "Correct Usage : python chess_board.py <SourceFilename> <NumberOfInitialVertices>"
	exit()

# Reading the image file
img = cv2.imread(sys.argv[1])
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

# Function to get distance between two points in 2-D plane
def get_dist((x1,y1), (x2,y2)):
	return int(sqrt( (y2-y1)**2 + (x2-x1)**2 ))

def get_midPoint((x1,y1), (x2,y2)):
	return ( int((x1+x2)/2) , int((y1+y2)/2) )

def populate(SP, EP):
	ls = [(0,0) for x in range(FACTOR+1)]
	ls[0] = SP
	ls[8] = EP
	ls[4] = get_midPoint(ls[0],ls[8])
	ls[2] = get_midPoint(ls[0],ls[4])
	ls[1] = get_midPoint(ls[0],ls[2])
	ls[3] = get_midPoint(ls[2],ls[4])
	ls[6] = get_midPoint(ls[4],ls[8])
	ls[5] = get_midPoint(ls[4],ls[6])
	ls[7] = get_midPoint(ls[8],ls[6])
	return ls


# Detecting vertices in the image
corners = cv2.goodFeaturesToTrack(gray,int(sys.argv[2]),0.01,10)
corners = np.int0(corners)

vertices = []

# Pushing the detected vertices in the list
for i in corners:
	x,y = i.ravel()
	vertices.append((x,y))
	# Initially detected points
	#cv2.circle(img,(x,y),2,RED,-1)
	#print x," ",y

#print "^"*30
#plt.imshow(img),plt.show()

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
		#print point
		if point[0] > top_right_x:
			top_right_x,top_right_y = point[0],point[1]
		if point[0] < top_left_x:
			top_left_x,top_left_y = point[0],point[1]
	if(point[1] >= maxxy - OFFSET and point[1] <= maxxy + OFFSET):
		#print point
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

# Image with borders made
#plt.imshow(img),plt.show()
# cv2.imwrite("border.jpg",img);

# Trying to get more precise points on left line
left_line = populate( (top_left_x,top_left_y) , (bottom_left_x,bottom_left_y) )

top_line = populate( (top_left_x,top_left_y) , (top_right_x, top_right_y) )

bottom_line = populate( (bottom_left_x,bottom_left_y), (bottom_right_x, bottom_right_y) )

right_line = populate(  (top_right_x,top_right_y) , (bottom_right_x, bottom_right_y) )


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
	# New Vertices made on board
	#cv2.circle(img,(x,y),2,RED,-1)
	new_vertices.append((x,y))

# Matrix to store coordinates of vertices on the board
matrix = [[(0,0) for x in range(FACTOR+2)] for x in range(FACTOR+2)]

topology = [["." for x in range(FACTOR)] for x in range(FACTOR)]

# Filling the matrix
matrix[0][0] = (top_left_x,top_left_y)

for i in range(0,FACTOR):
	for j in range(0,FACTOR):
		predicted_x = matrix[i][j][0] + int( (right_line[i][0] - left_line[i][0]) / 8 )
		predicetd_y = matrix[i][j][1] + int( (bottom_line[j][1] - top_line[j][1]) / 8 )

		# Predicted points
		#cv2.circle(img,(predicted_x,matrix[i][j][1]),5,RED,-1)
		#cv2.circle(img,(matrix[i][j][0],predicetd_y),5,RED,-1)

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

matrix[FACTOR][FACTOR] = (bottom_right_x,bottom_right_y)

# Predicted Vertices plotted on image
#cv2.imwrite("predicted.jpg",img)

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
		cv2.circle(img,(matrix[i][j][0],matrix[i][j][1]),5,BLUE,-1)

# Final grid on image
#plt.imshow(img),plt.show()

# Taking out each cell and deciding if :
# 1> it is empty
# 2> it has a black piece
# 3> it has a white piece
for i in range(0,FACTOR):
	for j in range(0,FACTOR):
		filename = str(i)+str(j)+".jpg"

		cropped = img[matrix[i][j][1]+5:matrix[i+1][j+1][1]-5 ,matrix[i][j][0]+5:matrix[i+1][j+1][0]-5]
		#cropped = img[matrix[i][j][1]:matrix[i+1][j+1][1] ,matrix[i][j][0]:matrix[i+1][j+1][0]]
		cv2.imwrite(filename,cropped)
		shutil.move(filename,"temp/"+filename)
		
		cropped = img[matrix[i][j][1]+5:matrix[i+1][j+1][1]-5 ,matrix[i][j][0]+5:matrix[i+1][j+1][0]-5]

		c = 0
		white = 0
		black = 0
		tot = 0
		for row in cropped:
			for p in row:
				c+=1
				tot = tot + p[0] + p[1] + p[2]
				if p[0]<=BLACK_THRESHOLD and p[1]<=BLACK_THRESHOLD and p[2]<=BLACK_THRESHOLD:
					black+=1
				if p[0]>=WHITE_THRESHOLD and p[1]>=WHITE_THRESHOLD and p[2]>=WHITE_THRESHOLD:
					white+=1
		probW = (white*1.0)/(c*1.0)
		probB = (black*1.0)/(c*1.0)

		# Probability of white piece and black piece at every cell
		print i," ",j," ",int(probW*100)," ",int(probB*100)," ",int(tot/c)

		if(probW > PROBABILITY_THRESHOLD):
			topology[i][j] = 'W'
		elif probB > PROBABILITY_THRESHOLD:
			topology[i][j] = 'B'
		

# Printing the final board state
for i in range(0,FACTOR):
	for j in range(0,FACTOR):
		print topology[i][j],
	print ""

# Final grid on image
plt.imshow(img),plt.show()
#cropped = img[top_left_y:bottom_right_y ,top_left_x:bottom_right_x]
#cv2.imwrite("_grid.jpg",cropped)
#cv2.imwrite("grid.jpg",img)