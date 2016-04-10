#! /usr/bin/bash

i=30
garbage=1

# python camera.py blankBoard
# python camera.py fix

while true; do
	python test.py img/blankBoard.jpg img/fix.jpg 200 $i > thisPlayerMatrix.txt
	cat thisPlayerMatrix.txt
	./checkBlack

	if [ $? -eq 0 ]
	then
		# echo "here"
		echo $i > tempFile.txt
		exit
	fi
	i=$((i - 1))
done