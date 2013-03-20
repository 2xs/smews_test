#!/bin/bash
# $1: ip
# $2: get url
# $3: expected http code (200 if omitted)
# $4: path to a file that should be equivalent to the downloaded file
# return true if the expected http code is returned by smews

out_file="/dev/null"
if [ $# -ge 4 ]
then
    out_file=`mktemp /tmp/tmp.XXXXXXXX`
fi

CURL="curl -s -S -g --connect-timeout 3 --retry 2 --max-time 3 -o $out_file -w %{http_code}"

ip_addr=$1
if echo $ip_addr | grep -q ':'
then
    ip_addr="[$ip_addr]" # ipv6 must be in square brackets in url
fi

HTTP_CODE=`$CURL http://$ip_addr/$2`
CURL_EXIT_CODE=$?
if [ $CURL_EXIT_CODE -ne 0 ]
then
    exit $CURL_EXIT_CODE
fi

REQUEST_CODE=$3

if [ -z "$REQUEST_CODE" ]
then
    REQUEST_CODE=200
fi
if [ $HTTP_CODE = $REQUEST_CODE ]
then
    if ! [ $out_file = "/dev/null" ]
    then
	if file $out_file | grep -q "gzip"
	then
	    gunzip -c $out_file | diff - $4 > /dev/null
	else
	    diff $out_file $4 > /dev/null
	fi
	exit_code=$?
	rm -f $out_file
	exit $exit_code
    fi
    exit 0
fi

exit 100
