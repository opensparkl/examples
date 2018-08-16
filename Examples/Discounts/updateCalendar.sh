#!/bin/bash
# Call with two arguments: SPARKL instance URL and SPARKL username
# For example:
# ./updateCalendar.sh http://localhost:8000 admin@sparkl.com
URL=$1
USER=$2

sparkl connect ${URL}
sparkl login ${USER} 
echo logged into ${URL} as ${USER}
sparkl vars -r bulk Backup.erl
echo Using Backup.erl to update Discounts calendar 
sparkl call Scratch/DiscountsCalendar/Mix/API/BulkFeed
sparkl logout
sparkl close 