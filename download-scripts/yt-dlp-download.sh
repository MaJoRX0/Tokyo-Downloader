#!/bin/bash

file=$1

while read -r line; do
	IFS='|' read -ra array <<< $line
	yt-dlp -o "${array[1]}" ${array[0]}
done < "$file"

