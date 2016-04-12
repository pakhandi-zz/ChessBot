'''
	Author : Asim Krishna Prasad

	Aim : 
		1> Take image of blank board
		2> Identify the board
		3> Separate each cell
		4> Fix threshold for each cell
		5> Take another board
		6> Predict the color of piece on each cell if not empty
		7> Return the current player matrix

	Gives correct output for X2, X3, X4, X6, X7
	X1 : One cell error
	X5 : corners not correct

'''
import numpy as np
import cv2
import sys
from matplotlib import pyplot as plt
from math import *
import shutil
import Geometry
from copy import deepcopy
from PIL import Image

class ChessBoard:
	# Colors
	RED   = (255,0,0)
	GREEN = (0,255,0)
	BLUE  = (0,0,255)

	# Number of cells to be detected
	FACTOR = 8

	# A very high value
	INT_MAX = 1000000009

	# Number of vertices to be detected for final detection of all vertices
	FINAL_VERTICES_COUNT = 150

	# Amount of relaxation allowed in y-axis detection of corners
	OFFSET = 0

	# Offset to decide number of pixels to consider for each cell
	OFFSET2 = 5

	# Number of vertices to be detected for initial detection of corners
	INITIAL_VERTICES_COUNT = None

	# The image to be processed and it's grayscale
	gray = None

	# The images of blank board and full board
	blankBoard = None
	fullBoard = None

	# Images after edge detection
	blankBoardEdges = None
	fullBoardEdges = None

	# to save the pixel values of empty board and full board
	blankBoardMatrix = []
	fullBoardMatrix = []

	# List of all vertices that lie on border
	OUTER_VERTICES = []

	# List for all the vertices detected on board at the end
	ALL_VERTICES = []

	# The four corners on the board
	CORNERS = []

	# The topology after probability calculation
	TOPOLOGY = []

	# name of the files
	blankName = "blankBoard"
	fullName = "fullBoard"

	# black threshold
	blackThreshold = 0

	def __init__(self, blankBoard, fullBoard, InitialVerticesCount, blackThreshold, FinalVerticesCount = 150, Offset = 15):
		
		self.INITIAL_VERTICES_COUNT = InitialVerticesCount
		self.FINAL_VERTICES_COUNT = FinalVerticesCount
		self.OFFSET = Offset
		self.blackThreshold = blackThreshold

		self.blankBoard = cv2.imread(blankBoard)
		self.fullBoard = cv2.imread(fullBoard)
		
		self.blankBoardEdges = cv2.Canny(self.blankBoard,0,100)
		self.fullBoardEdges = cv2.Canny(self.fullBoard,0,100)

		self.detectFourCorners(self.blankBoardEdges)
		self.blankBoardMatrix = self.process(self.blankBoard, self.blankBoardEdges, self.blankName)
		self.fullBoardMatrix = self.process(self.fullBoard, self.fullBoardEdges,self.fullName)

	def sharpen(self,testImg):
		#Create the identity filter, but with the 1 shifted to the right!
		kernel = np.zeros( (9,9), np.float32)
		kernel[4,4] = 2.0   #Identity, times two! 

		#Create a box filter:
		boxFilter = np.ones( (9,9), np.float32) / 81.0

		#Subtract the two:
		kernel = kernel - boxFilter

		custom = cv2.filter2D(testImg, -1, kernel)

		return testImg

	def process(self, testImg, testImgEdges, folderName):
		# self.detectFourCorners(testImgEdges)
		self.plotFourCorners(testImg)
		# plt.imshow(testImg),plt.show()
		self.plotOuterEdges(testImg)
		# plt.imshow(testImg),plt.show()
		self.detectVerticesOnOuterEdges()
		self.plotAllEdges(testImg)
		# plt.imshow(testImg),plt.show()
		self.detectAllVertices(testImg)
		# self.displayAllVertices(testImg)
		# print folderName
		return self.populate(testImg, folderName)

	def detectFourCorners(self, testImgEdges):

		self.CORNERS = []

		INITIAL_VERTICES = cv2.goodFeaturesToTrack(testImgEdges,int(self.INITIAL_VERTICES_COUNT),0.03,10)
		INITIAL_VERTICES = np.int0(INITIAL_VERTICES)

		vertices = []

		# tempImg = deepcopy(self.fullBoard)

		# print "="*20

		# allDetectedPoints = []

		for i in INITIAL_VERTICES:
			x,y = i.ravel()
			# allDetectedPoints.append((x,y))
			vertices.append((x,y))
			# cv2.circle(tempImg,(x,y),3,self.GREEN,-1)
		# plt.imshow(tempImg),plt.show()

		# allDetectedPoints.sort()

		# for point in allDetectedPoints:
		# 	print point

		# print "="*20

		# Variables to store four corners of the board
		bottom_left_x = self.INT_MAX
		bottom_left_y = 0

		top_left_x = self.INT_MAX
		top_left_y = self.INT_MAX

		bottom_right_x = 0
		bottom_right_y = 0

		top_right_x = 0
		top_right_y = self.INT_MAX

		minny = self.INT_MAX
		maxxy = 0

		# Detecting the four corners of the board
		# ---------------------------------------------------------------------------

		for point in vertices:
			minny = min(point[1],minny)
			maxxy = max(point[1],maxxy)

		# print (minny,maxxy)

		# print "*"*20

		for point in vertices:
			if(point[1] >= minny - self.OFFSET and point[1] <= minny + self.OFFSET):
				# print point
				if point[0] > top_right_x:
					# to avoid any other vertex on edge to be detected as the corner
					if point[1] - top_right_y < point[0] - top_right_x:
						top_right_x,top_right_y = point[0],point[1]
				if point[0] < top_left_x:
					top_left_x,top_left_y = point[0],point[1]
			if(point[1] >= maxxy - self.OFFSET and point[1] <= maxxy + self.OFFSET):
				# print point
				if point[0] > bottom_right_x:
					bottom_right_x,bottom_right_y = point[0],point[1]
				if point[0] < bottom_left_x:
					# print point
					bottom_left_x,bottom_left_y = point[0],point[1]
					# print bottom_left_x," ",bottom_left_y

		# print "*"*20

		self.CORNERS.append((bottom_left_x,bottom_left_y))
		self.CORNERS.append((top_left_x,top_left_y))
		self.CORNERS.append((top_right_x,top_right_y))
		self.CORNERS.append((bottom_right_x,bottom_right_y))

	def plotFourCorners(self, testImg):
		tempImg = testImg
		for point in self.CORNERS:
			cv2.circle(tempImg,point,3,self.RED,-1)

	def plotOuterEdges(self, testImg):
		tempImg = testImg
		for i in range(0,4):
			cv2.line(tempImg, (self.CORNERS[i]), (self.CORNERS[(i+1)%4]), self.GREEN, 2 )

	def detectVerticesOnOuterEdges(self):
		self.OUTER_VERTICES = []
		for i in range(0,4):
			self.OUTER_VERTICES.append( Geometry.partitionLine((self.CORNERS[i]), (self.CORNERS[(i+1)%4]), self.FACTOR) )

	def plotAllEdges(self, testImg):
		for j in range(0,2):
			for i in range(0,self.FACTOR+1):
				cv2.line(testImg, (self.OUTER_VERTICES[j][i]) , (self.OUTER_VERTICES[j+2][self.FACTOR - i]), self.RED , 1)

	def detectAllVertices(self, testImg):
		# Detecting vertices on the newly constructed board
		self.gray = cv2.cvtColor(testImg,cv2.COLOR_BGR2GRAY)

		tempVertices = cv2.goodFeaturesToTrack(self.gray,int(self.FINAL_VERTICES_COUNT),0.01,10)
		tempVertices = np.int0(tempVertices)

		newVertices = []

		for i in tempVertices:
			x,y = i.ravel()
			newVertices.append((x,y))

		# Matrix to store coordinates of vertices on the board
		self.ALL_VERTICES = [[(0,0) for x in range(self.FACTOR+2)] for x in range(self.FACTOR+2)]

		# Filling the matrix
		self.ALL_VERTICES[0][0] = (self.CORNERS[1])

		for i in range(0,self.FACTOR):
			for j in range(0,self.FACTOR):
				predicted_x = self.ALL_VERTICES[i][j][0] + int( ( self.OUTER_VERTICES[2][self.FACTOR - i][0] - self.OUTER_VERTICES[0][i][0] ) / 8 )
				predicted_y = self.ALL_VERTICES[i][j][1] + int( ( self.OUTER_VERTICES[3][self.FACTOR - i][1] - self.OUTER_VERTICES[1][i][1] ) / 8 )

				minn_dist = self.INT_MAX

				for point in newVertices:
					this_dist = Geometry.getPointsDistance( point , (predicted_x, self.ALL_VERTICES[i][j][1])  )
					if this_dist < minn_dist:
						self.ALL_VERTICES[i][j+1] = point
						minn_dist = this_dist

				minn_dist = self.INT_MAX

				for point in newVertices:
					this_dist = Geometry.getPointsDistance( point , (self.ALL_VERTICES[i][j][0], predicted_y)  )
					if this_dist < minn_dist:
						self.ALL_VERTICES[i+1][j] = point;
						minn_dist = this_dist

		self.ALL_VERTICES[self.FACTOR][self.FACTOR] = (self.CORNERS[3])

	def createTopology(self):
		# Taking out each cell and deciding if :
		# 1> it is empty
		# 2> it has a black piece
		# 3> it has a white piece

		self.TOPOLOGY = [["." for x in range(self.FACTOR)] for x in range(self.FACTOR)]


		blank = []
		full = []

		for i in xrange(8):
			for j in xrange(8):
				img = Image.open("blankBoard/" + str(i) + str(j) + ".jpg")
				img = img.convert("L")
				clrs = img.getcolors()
				for ind in xrange(len(clrs)):
					clrs[ind] = (clrs[ind][1], clrs[ind][0])
				clrs.sort()
				# print i, j, clrs[0][0], clrs
				blank.append( (clrs[0][0]) )
				# if sum(img.convert("L").getextrema()) in (0, 2):
				# 	print str(i) + str(j)

		# print "$" * 30

		for i in xrange(8):
			for j in xrange(8):
				img = Image.open("fullBoard/" + str(i) + str(j) + ".jpg")
				img = img.convert("L")
				clrs = img.getcolors()
				for ind in xrange(len(clrs)):
					clrs[ind] = (clrs[ind][1], clrs[ind][0])
				clrs.sort()
				# print i, j, clrs[0][0], clrs
				full.append( (clrs[0][0] )  )

		matF = [[0 for i in xrange(self.FACTOR)] for i in xrange(self.FACTOR)]
		matB = [[0 for i in xrange(self.FACTOR)] for i in xrange(self.FACTOR)]

		for i in xrange(len(full)):
			# print self.blackThreshold
			thisOffset = int(self.blackThreshold)
			# print full[i], " ", blank[i] 
			# if (i / 8) <= 3:
			# 	thisOffset = 10
			# elif (i / 8) <= 5:
			# 	thisOffset = 5
			# else:
			# 	thisOffset = 2
			x = i / 8
			y = i % 8
			matF[x][y] = full[i]
			matB[x][y] = blank[i]
			if abs(full[i] - blank[i]) >= thisOffset:
				self.TOPOLOGY[x][y] = 'W'

				if(full[i] < blank[i]):
					self.TOPOLOGY[x][y] = 'B'

		# for i in xrange(self.FACTOR):
		# 	for j in xrange(self.FACTOR):
		# 		print("%5d" % (matB[i][j]) ) ,
		# 	print ""

		# print ""

		# for i in xrange(self.FACTOR):
		# 	for j in xrange(self.FACTOR):
		# 		print("%5d" % (matF[i][j]) ) ,
		# 	print ""

		

		return

	def getFourCorners(self):
		return self.CORNERS

	def getAllVertices(self):
		return self.ALL_VERTICES

	def getTopology(self):
		return self.TOPOLOGY

	def displayFourCorners(self, testImg):
		tempImg = deepcopy(testImg)
		for point in self.CORNERS:
			cv2.circle(tempImg,point,3,self.RED,-1)
		plt.imshow(tempImg),plt.show()

	def displayFourEdges(self, testImg):
		tempImg = deepcopy(testImg)
		for i in range(0,4):
			cv2.line(tempImg, (self.CORNERS[i]), (self.CORNERS[(i+1)%4]), self.GREEN, 2 )
		plt.imshow(tempImg),plt.show()

	def displayAllEdges(self, testImg):
		tempImg = deepcopy(testImg)
		for j in range(0,2):
			for i in range(0,self.FACTOR+1):
				cv2.line(tempImg, (self.OUTER_VERTICES[j][i]) , (self.OUTER_VERTICES[j+2][self.FACTOR - i]), self.RED , 1)
		plt.imshow(tempImg),plt.show()

	def displayAllVertices(self, testImg):
		tempImg = deepcopy(testImg)
		for i in range(0,self.FACTOR+1):
			for j in range(0,self.FACTOR+1):
				cv2.circle(tempImg,(self.ALL_VERTICES[i][j]),5,self.BLUE,-1)
		plt.imshow(tempImg),plt.show()

	def displayTopology(self):
		for i in range(0,self.FACTOR):
			for j in range(0,self.FACTOR):
				sys.stdout.write(self.TOPOLOGY[i][j])
				#print self.TOPOLOGY[i][j],""
			print ""

	def populate(self, testImg, folderName):
		thisMatrix = [[[[(0) for x in range(10)] for x in range(10)] for x in range(self.FACTOR)] for x in range(self.FACTOR)]
		tempImg = testImg
		# print folderName
		for x in range(0,self.FACTOR):
			for y in range(0,self.FACTOR):
				cropped = tempImg[self.ALL_VERTICES[x][y][1]+5:self.ALL_VERTICES[x+1][y+1][1]-5 ,self.ALL_VERTICES[x][y][0]+5:self.ALL_VERTICES[x+1][y+1][0]-5]
				cropped = self.sharpen(cropped)

				# plt.imshow(cropped),plt.show()

				height = len(cropped)
				width = len(cropped[0])

				width = int(width / 2)
				height = int(height / 2)

				cropped = cropped[height-5:height+5, width-5:width+5]
				cropped = self.sharpen(cropped)
				thisMatrix[x][y] = cropped

				filename = str(x) + str(y) + ".jpg"

				cv2.imwrite(filename,cropped)
				shutil.move(filename,folderName+"/"+filename)

		return thisMatrix