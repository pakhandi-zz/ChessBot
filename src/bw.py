import numpy as np
import cv2
import sys
from matplotlib import pyplot as plt
from math import *
import shutil
import Geometry
from copy import deepcopy
from PIL import Image

blank = []
full = []

for i in xrange(8):
	for j in xrange(8):
		img = Image.open("blankBoard/" + str(i) + str(j) + ".jpg")
		img = img.convert("L")
		clrs = img.getcolors()
		clrs.sort(reverse = True)
		blank.append(clrs[0][1])
		# if sum(img.convert("L").getextrema()) in (0, 2):
		# 	print str(i) + str(j)

for i in xrange(8):
	for j in xrange(8):
		img = Image.open("fullBoard/" + str(i) + str(j) + ".jpg")
		img = img.convert("L")
		clrs = img.getcolors()
		clrs.sort(reverse = True)
		full.append(clrs[0][1])

for i in xrange(len(full)):
	print blank[i], " ", full[i]

for i in xrange(len(full)):
	if abs(full[i] - blank[i]) >= 5:
		print i