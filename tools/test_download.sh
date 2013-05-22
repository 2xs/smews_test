#!/bin/bash

function usage()
{
    echo "Usage: $0 [options] <ip> <url>" 1>&2
    echo "Options:" 1>&2
    echo "   * -c <code>: the expected http code (will return 100 if the return http code is not equal to the option. 200 is used as default" 1>&2
    echo "   * -v <checkfile>: validates the downloaded response against a given file, return an error code if files differ" 1>&2
    echo "   * -p <form_data>: use post method. This directly use <form_data> as the -F option of curl. see curl man page for information on this option" 1>&2
    echo "   * -t <timeout>: curl timeout in second (default 3)" 1>&2
    echo "   * -r <retry>: curl max retries (default 2)" 1>&2
}

if [ $# -eq 0 ]
then
    usage $0
    exit 1
fi

request_code=200
out_file="/dev/null"
check_file=""
post_parameters=""
post_file=""
timeout="3"
retry="3"

while getopts "c:v:p:t:r:" opt;
do
    case $opt in
	"c")
	    request_code="$OPTARG"
	    ;;
	"v")
	    check_file="$OPTARG"
	    out_file=`mktemp /tmp/tmp.XXXXXXXX`
	    ;;
	"p")
	    post_parameters="$OPTARG"
	    ;;
	"t")
	    timeout="$OPTARG"
	    ;;
	"r")
	    retry="$OPTARG"
	    ;;
	'?')
	    usage $0
	    exit 1
	    ;;
    esac
done
# Removes options
shift $((OPTIND-1))

if [ $# -ne 2 ]
then
    usage $0
    exit 1
fi

curl_cmd="curl -s -S -g --connect-timeout $timeout --retry $retry --max-time $timeout -o $out_file -w %{http_code}"
if ! [ -z "$post_parameters" ]
then
    curl_cmd="$curl_cmd -F $post_parameters"
fi

ip_addr=$1
if echo $ip_addr | grep -q ':'
then
    ip_addr="[$ip_addr]" # ipv6 must be in square brackets in url
fi

http_code=`$curl_cmd http://$ip_addr/$2`
curl_exit_code=$?
if [ $curl_exit_code -ne 0 ]
then
    exit $curl_exit_code
fi

if [ $http_code = $request_code ]
then
    if ! [ $out_file = "/dev/null" ]
    then
	if file $out_file | grep -q "gzip"
	then
	    gunzip -c $out_file | diff - $check_file > /dev/null
	else
	    diff $out_file $check_file > /dev/null
	fi
	exit_code=$?
	rm -f $out_file
	exit $exit_code
    fi
    exit 0
fi

exit 100
