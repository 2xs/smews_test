#!/bin/bash

# $1: ip
# $2: target
# $3: get url

CURL="curl -g --connect-timeout 2 --max-time 3"

ip_addr=$1
if echo $ip_addr | grep -q ':'
then
    ip_addr="[$ip_addr]" # ipv6 must be in square brackets in url
fi


if ! $CURL  http://$ip_addr/$3 >& /dev/null
then
    exit 1
fi
exit 0
