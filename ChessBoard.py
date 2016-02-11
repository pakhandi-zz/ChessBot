import numpy as np
import cv2
import sys
from matplotlib import pyplot as plt
from math import *
import shutil
import Geometry

class ChessBoard:
	RED   = (255,0,0)
	GREEN = (0,255,0)
	BLUE  = (0,0,255)

	FACTOR = 8
	INT_MAX = 1000000009

	FINAL_VERTICES_COUNT = 150
	OFFSET = 10

	WHITE_THRESHOLD = 142
	BLACK_THRESHOLD = 80

	PROBABILITY_THRESHOLD = 0.13

	SOURCE_FILE = None
	INITIAL_VERTICES_COUNT = None

	img = None
	gray = None

	INITIAL_VERTICES = []
	FINAL_VERTICES = []

	OUTER_VERTICES = []
	ALL_VERTICES = []

	CORNERS = []
	TOPOLOGY = []

	def __init__(self, SourceFile, InitialVerticesCount, FinalVerticesCount = 150, Offset = 10, WhiteThreshold = 142, BlackThreashold = 80, ProbabilityThreshold = 0.13):
		
		self.SOURCE_FILE = SourceFile
		self.INITIAL_VERTICES_COUNT = InitialVerticesCount

		self.img = cv2.imread(self.SOURCE_FILE)
		self.gray = cv2.cvtColor(self.img,cv2.COLOR_BGR2GRAY)

		self.FINAL_VERTICES_COUNT = FinalVerticesCount
		self.OFFSET = Offset

		self.WHITE_THRESHOLD = WhiteThreshold
		self.BLACK_THRESHOLD = BlackThreashold
		self.PROBABILITY_THRESHOLD = ProbabilityThreshold

		self.INITIAL_VERTICES = cv2.goodFeaturesToTrack(self.gray,int(self.INITIAL_VERTICES_COUNT),0.03,10)
		self.INITIAL_VERTICES = np.int0(self.INITIAL_VERTICES)

	def detectFourCorners(self):

		vertices = []

		tempImg = self.img[:]

		for i in self.INITIAL_VERTICES:
			x,y = i.ravel()
			cv2.circle(tempImg,(x,y),3,self.RED,-1)
			vertices.append((x,y))

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

		for point in vertices:
			if(point[1] >= minny - self.OFFSET and point[1] <= minny + self.OFFSET):
				#print point
				if point[0] > top_right_x:
					top_right_x,top_right_y = point[0],point[1]
				if point[0] < top_left_x:
					top_left_x,top_left_y = point[0],point[1]
			if(point[1] >= maxxy - self.OFFSET and point[1] <= maxxy + self.OFFSET):
				#print point
				if point[0] > bottom_right_x:
					bottom_right_x,bottom_right_y = point[0],point[1]
				if point[0] < bottom_left_x:
					bottom_left_x,bottom_left_y = point[0],point[1]

		self.CORNERS.append((bottom_left_x,bottom_left_y))
		self.CORNERS.append((top_left_x,top_left_y))
		self.CORNERS.append((top_right_x,top_right_y))
		self.CORNERS.append((bottom_right_x,bottom_right_y))

	def plotFourCorners(self):
		tempImg = self.img
		for point in self.CORNERS:
			cv2.circle(tempImg,point,3,self.RED,-1)

	def plotOuterEdges(self):
		tempImg = self.img
		for i in range(0,4):
			cv2.line(tempImg, (self.CORNERS[i]), (self.CORNERS[(i+1)%4]), self.GREEN, 2 )

	def detectVerticesOnOuterEdges(self):
		for i in range(0,4):
			self.OUTER_VERTICES.append( Geometry.partitionLine((self.CORNERS[i]), (self.CORNERS[(i+1)%4]), self.FACTOR) )

	def plotAllEdges(self):
		for j in range(0,2):
			for i in range(0,self.FACTOR+1):
				cv2.line(self.img, (self.OUTER_VERTICES[j][i]) , (self.OUTER_VERTICES[j+2][self.FACTOR - i]), self.RED , 1)

	def detectAllVertices(self):
		# Detecting vertices on the newly constructed board
		self.gray = cv2.cvtColor(self.img,cv2.COLOR_BGR2GRAY)

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

		for i in range(0,self.FACTOR):
			for j in range(0,self.FACTOR):
				filename = str(i)+str(j)+".jpg"

				cropped = self.img[self.ALL_VERTICES[i][j][1]+5:self.ALL_VERTICES[i+1][j+1][1]-5 ,self.ALL_VERTICES[i][j][0]+5:self.ALL_VERTICES[i+1][j+1][0]-5]
				#cropped = img[matrix[i][j][1]:matrix[i+1][j+1][1] ,matrix[i][j][0]:matrix[i+1][j+1][0]]
				cv2.imwrite(filename,cropped)
				shutil.move(filename,"temp/"+filename)
				
				cropped = self.img[self.ALL_VERTICES[i][j][1]+5:self.ALL_VERTICES[i+1][j+1][1]-5 ,self.ALL_VERTICES[i][j][0]+5:self.ALL_VERTICES[i+1][j+1][0]-5]

				c = 0
				white = 0
				black = 0
				tot = 0
				for row in cropped:
					for p in row:
						c+=1
						tot = tot + p[0] + p[1] + p[2]
						if p[0]<=self.BLACK_THRESHOLD and p[1]<=self.BLACK_THRESHOLD and p[2]<=self.BLACK_THRESHOLD:
							black+=1
						if p[0]>=self.WHITE_THRESHOLD and p[1]>=self.WHITE_THRESHOLD and p[2]>=self.WHITE_THRESHOLD:
							white+=1
				probW = (white*1.0)/(c*1.0)
				probB = (black*1.0)/(c*1.0)

				# Probability of white piece and black piece at every cell
				print i," ",j," ",int(probW*100)," ",int(probB*100)," ",int(tot/c)

				if(probW > self.PROBABILITY_THRESHOLD):
					self.TOPOLOGY[i][j] = 'W'
				elif probB > self.PROBABILITY_THRESHOLD:
					self.TOPOLOGY[i][j] = 'B'

	def getFourCorners(self):
		return self.CORNERS

	def getAllVertices(self):
		return self.ALL_VERTICES

	def getTopology(self):
		return self.TOPOLOGY

	def displayFourCorners(self):
		tempImg = cv2.imread(self.SOURCE_FILE)
		for point in self.CORNERS:
			cv2.circle(tempImg,point,3,self.RED,-1)
		plt.imshow(tempImg),plt.show()

	def displayFourEdges(self):
		tempImg = cv2.imread(self.SOURCE_FILE)
		for i in range(0,4):
			cv2.line(tempImg, (self.CORNERS[i]), (self.CORNERS[(i+1)%4]), self.GREEN, 2 )
		plt.imshow(tempImg),plt.show()

	def displayAllEdges(self):
		tempImg = cv2.imread(self.SOURCE_FILE)
		for j in range(0,2):
			for i in range(0,self.FACTOR+1):
				cv2.line(tempImg, (self.OUTER_VERTICES[j][i]) , (self.OUTER_VERTICES[j+2][self.FACTOR - i]), self.RED , 1)
		plt.imshow(tempImg),plt.show()

	def displayAllVertices(self):
		tempImg = cv2.imread(self.SOURCE_FILE)
		for i in range(0,self.FACTOR+1):
			for j in range(0,self.FACTOR+1):
				cv2.circle(tempImg,(self.ALL_VERTICES[i][j]),5,self.BLUE,-1)
		plt.imshow(tempImg),plt.show()

	def displayTopology(self):
		for i in range(0,self.FACTOR):
			for j in range(0,self.FACTOR):
				print self.TOPOLOGY[i][j],
			print ""


