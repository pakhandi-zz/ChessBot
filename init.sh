#! /usr/bin/bash

'''

	This is where the program starts
	This script is the driver and does following things :
	1> fixThreshold
	2> initialize the prevBoard.txt
	3> run play.sh

'''

sh fixThreshold.sh

cat initBoard.txt > prevBoard.txt
prev=""
while read line           
do            
    echo $line
    break         
done <thresholdVal.txt

sh play.sh $line