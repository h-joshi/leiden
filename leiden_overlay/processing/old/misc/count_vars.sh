#! /usr/bin/env bash

cd ../../dat/

COUNT=0
for f in `ls *.vcf`; do
	name="${f%.*}"
	((--COUNT))
	curr=`wc -l < $name.txt`
	COUNT=`expr $COUNT + $curr`
	echo `expr $curr - 1`  $name	
done
echo $COUNT
