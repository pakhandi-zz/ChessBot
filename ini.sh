#! /usr/bin/bash

# python camera.py blankBoard

i=0
garbage=1

while true; do
	read garbage
	python camera.py $i
	python test.py img/blankBoard.jpg img/$i.jpg 200 17 > thisPlayerMatrix.txt
	# ./rotateBaord > tempFile
	# cat tempFile > thisPlayerMatrix
	./generateBoard < thisPlayerMatrix.txt
	cat tempFile.txt > prevBoard.txt
	# read garbage
	./nextMove < prevBoard.txt
	i=$((i + 1))
done