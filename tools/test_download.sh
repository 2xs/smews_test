#!/bin/bash

# $1: ip
# $2: get url
# $3: expected http code (200 if omitted)
# return true if the expected http code is returned by smews

CURL="curl -s -S -g --connect-timeout 3 --retry 2 --max-time 3 -o /dev/null -w %{http_code}"

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
    exit 0
fi

exit 100
