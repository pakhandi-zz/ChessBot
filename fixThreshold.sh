#! /usr/bin/bash

i=60
garbage=1
down=0
up=50

# python camera.py blankBoard 1
# python camera.py fix 1


while true; do
	python test.py img/blankBoard.jpg img/fix.jpg 600 $i > thisPlayerMatrix.txt
	echo $i
	cat thisPlayerMatrix.txt
	echo "=============================="
	./checkBlack < thisPlayerMatrix.txt
	if [ $? -eq 0 ]
	then
		up=$i
		break
	fi
	i=$((i - 1))
done

i=0

while true; do
	python test.py img/blankBoard.jpg img/fix.jpg 600 $i > thisPlayerMatrix.txt
	echo $i
	cat thisPlayerMatrix.txt
	echo "=============================="
	./checkBlack < thisPlayerMatrix.txt
	if [ $? -eq 0 ]
	then
		down=$i
		break
	fi
	i=$((i + 1))
done

echo $down

echo $((down)) > thresholdVal.txt