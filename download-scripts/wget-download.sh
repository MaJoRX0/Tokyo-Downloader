#!/bin/bash

file=$1

while read -r line; do
	IFS='|' read -ra array <<< $line
	wget ${array[0]} -O "${array[1]}"
done < "$file"

