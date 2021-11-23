#!/bin/bash

echo 'Search bots:'
awk -F\" '{ print $6}' $1 | grep 'bot' | sort | uniq
