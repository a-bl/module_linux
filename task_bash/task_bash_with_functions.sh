#!/bin/bash

most_requested_ip() {
	echo 'Most requests were from IP:'
	awk '{ print $1 }' $1 | sort | uniq -c | sort -nr | head -n 1
}

most_popular_page() {
	echo 'Most popular page:'
	awk '{ print $7}' $1 | sort | uniq -c | sort -nr | head -n 1
}

request_per_ip() {
	echo 'Requests per IP:'
	awk '{ print $1 }' $1 | sort | uniq -c | sort -nr
}


non_existent_pages() {
	echo 'Non-existent pages clients were reffered to:'
	#sudo awk '{ if($9 == 404) { print $7 } }' $1 | sort | uniq
	awk '{ if ($9 !~ /2../) print $7, $9 }' $1 | sort | uniq -c | sort -gr
}

most_requested() {
	echo 'Most requested at:'
	awk '{ print $4 }' $1 | sed 's/\[//g' | cut -d: -f '1 2 3 4' | uniq -c | sort -nr | head -n 1
}

search_bots() {
	echo 'Search bots:'
	awk -F\" '{ print $6}' $1 | grep 'bot' | sort | uniq
}

if [ "$#" == "0" ];
then
        echo 'Expecting apache log file as an argument'
else
	echo '1. From which ip were the most requests?'
	most_requested_ip $1
	echo '2. What is the most requested page?'
	most_popular_page $1
	echo '3. How many requests were there from each ip?'
	request_per_ip $1
	echo '4. What non-existent pages were clients reffered to?'
	non_existent_pages $1
	echo '5. What time did site get the most requests?'
	most_requested $1
	echo '6. What search bots have accessed the site? (UA + IP)'
	search_bots $1
fi
