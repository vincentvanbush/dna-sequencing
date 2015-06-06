#!/bin/bash
files=("repeats_negative" "random_negative" "random_positive" "glitches_positive")
for i in "${files[@]}"; do
	cd $i
	for filename in *; do
		echo $filename
		python ../main.py $filename
	done
	cd ..
done



