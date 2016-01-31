'''
	Program to get live stream from secondary web cam and click a picture on press of a button
'''
import numpy as np
import cv2
import sys
import os
import shutil


# Checking arguments
if len(sys.argv) != 2:
	print "Correct Usage : python camera.py <DesiredFilename>"
	exit()

# the name for the file to be saved
filename = sys.argv[1] + ".jpg"

# 1 => to use secondary (USB) web camera
cap = cv2.VideoCapture(1)

while(True):
	# Capture frame-by-frame
	ret, frame = cap.read()

	# Our operations on the frame come here
	#gray = cv2.cvtColor(frame, cv2.COLOR)

	# Display the resulting frame
	cv2.imshow('frame',frame)

	#Save the frame and quit on 'q'
	if cv2.waitKey(1) & 0xFF == ord('q'):
		cv2.imwrite(filename,frame)
		if not os.path.exists("img/"):
			os.makedirs("img/")
		shutil.move(filename,"img/"+filename)
		break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()