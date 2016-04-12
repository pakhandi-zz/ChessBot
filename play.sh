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
	./nextMove < prevBoard.txt > out
	cat prevBoard.txt
	echo "======================="
	while read line           
	do            
	    echo $line
	    break         
	done <out
	python blue.py $line
	i=$((i + 1))
done