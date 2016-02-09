from math import *
# Function to get distance between two points in 2-D plane
def getPointsDistance((x1,y1), (x2,y2)):
	return int(sqrt( (y2-y1)**2 + (x2-x1)**2 ))

# Function to get mid-point of a line segment
def getMidPoint((x1,y1), (x2,y2)):
	return ( int((x1+x2)/2) , int((y1+y2)/2) )

# Function to get "Segments" equal segments on a line-segment
def partitionLine(SP, EP, Segments):
	Points = Segments + 1
	ls = [(0,0) for x in range(Points)]
	ls[0] = SP
	ls[8] = EP
	ls[4] = getMidPoint(ls[0],ls[8])
	ls[2] = getMidPoint(ls[0],ls[4])
	ls[1] = getMidPoint(ls[0],ls[2])
	ls[3] = getMidPoint(ls[2],ls[4])
	ls[6] = getMidPoint(ls[4],ls[8])
	ls[5] = getMidPoint(ls[4],ls[6])
	ls[7] = getMidPoint(ls[8],ls[6])
	return ls