#!/bin/bash

if [ "$#" == "0" ];
then
	echo 'Expecting apache log file as an argument'
else
	echo '1. From which ip were the most requests?'
	sudo ./1.sh $1
	echo '2. What is the most requested page?'
	sudo ./2.sh $1
	echo '3. How many requests were there from each ip?'
	sudo ./3.sh $1
	echo '4. What non-existent pages were clients reffered to?'
	sudo ./4.sh $1
	echo '5. What time did site get the most requests?'
	sudo ./5.sh $1
	echo '6. What search bots have accessed the site? (UA + IP)'
	sudo ./6.sh $1
fi
