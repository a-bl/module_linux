#!/bin/bash

echo 'Requests per IP:'
awk '{ print $1 }' $1 | sort | uniq -c | sort -nr
