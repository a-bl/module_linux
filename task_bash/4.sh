#!/bin/bash

echo 'Non-existent pages clients were reffered to:'
#sudo awk '{ if($9 == 404) { print $7 } }' $1 | sort | uniq
awk '{ if ($9 !~ /2../) print $7, $9 }' $1 | sort | uniq -c | sort -gr

#sudo awk -F '"' '{ print $3 " " $2}' $1 | awk '$1 != "200" { print $1" "$4 }' | sort | uniq -c | sort -gr
