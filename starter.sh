#!/bin/bash
files=("repeats_negative" "random_negative" "random_positive" "glitches_positive")
for i in "${files[@]}"; do
	cd $i 
	# we are in folder with specific instances
	rm -r tests/*
	for filename in *; do
		for j in `seq 1 2`;
		do
			python ../main.py $filename
		done
	done
	cd ..
done
