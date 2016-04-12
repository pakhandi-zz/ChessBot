#! /usr/bin/bash

# python camera.py blankBoard

i=0
garbage=1

while true; do
	read garbage
	python camera.py $i 0
	python test.py img/blankBoard.jpg img/$i.jpg 600 $1 > thisPlayerMatrix.txt
	# ./rotateBaord > tempFile
	# cat tempFile > thisPlayerMatrix
	./generateBoard < thisPlayerMatrix.txt
	cat tempFile.txt > prevBoard.txt
	cat prevBoard.txt
	echo "======================="
	./nextMove < prevBoard.txt
	cat prevBoard.txt
	echo "======================="
	i=$((i + 1))
done