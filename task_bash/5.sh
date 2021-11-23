#!/bin/bash

echo 'Most requested at:'
awk '{ print $4 }' $1 | sed 's/\[//g' | cut -d: -f '1 2 3 4' | uniq -c | sort -nr | head -1
