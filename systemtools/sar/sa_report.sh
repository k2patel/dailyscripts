#!/bin/bash
# Ketan Patel 
# MIT
 
# dtm=$(date -d 'now -1 days' +%d)
dtm=$(date -d 'now' +%d)
sar=$(which sar)
perl=$(which perl)
location='/location/for/script/folder'
 
cd $location
# $sar -q -b -d -u -p -r -n DEV -f /var/log/sa/sa$dtm > sa$dtm.txt
 
$sar -f /var/log/sa/sa$dtm > sa$dtm_1.txt
$sar -r -b -q -d -n DEV -I SUM -u -f /var/log/sa/sa$dtm > sa$dtm.txt
$perl sar2rrd.pl -t MDY -f sa$dtm_1.txt
$perl sar2rrd.pl -t MDY -f sa$dtm.txt
rm sa$dtm_1.txt
rm sa$dtm.txt

$python3 $location/notify.py 
