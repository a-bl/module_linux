#!/bin/bash

echo 'Most popular page:'
awk '{ print $7}' $1 | sort | uniq -c | sort -nr | head -n 1
