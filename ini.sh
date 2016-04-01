#! /usr/bin/bash

python camera.py blankBoard

i=0
garbage=1

while true; do
	read garbage
	python camera.py $i
	# python test.py img/blankBoard.jpg img/$i.jpg 200 > thisPlayerMatrix
	# ./rotateBaord > tempFile
	# cat tempFile > thisPlayerMatrix
	# ./generateBoard < thisPlayerMatrix > tempFile
	# cat tempFile > prevBoard
	# ./nextMove < prevBoard
	i=$((i + 1))
done