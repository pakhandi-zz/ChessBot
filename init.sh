#! /usr/bin/bash

sh fixThreshold.sh

cat initBoard.txt > prevBoard.txt
prev=""
while read line           
do            
    echo $line
    break         
done <thresholdVal.txt

sh play.sh $line