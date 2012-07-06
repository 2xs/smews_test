#!/bin/bash

# Kill smews and exit
# args: $1 return value
function clean_exit()
{
    kill_smews
    exit $1
}

# Kill smews
# return true if smews was running and false if not
function kill_smews()
{
    if ! pgrep smews.elf > /dev/null
    then
	return 1
    fi
    while pgrep smews.elf > /dev/null
    do
	sudo pkill smews.elf
    done
    return 0
}

# Display a fail test message
# args: $1: ip: $2: target remainder: message
function fail()
{
    echo -n "FAIL:$1:$2:" 1>&2
    shift 2
    echo $* 1>&2
}

# args: $1: ipaddr $2: target $3: additional apps
function build_smews()
{
    scons -c >& /dev/null
    if ! scons ipaddr=$1 apps=smews_check,$3 target=$2 debug=0 >& /dev/null
    then
	fail $1 $2 "BUILD"
	return 1
    fi
}

# args: $1 ip $2 target
function launch_smews()
{
    case $2 in
	linux)
	    sudo echo -n "" # This ensures that the password for sudo is prompted by a foreground command
	    if ! [ -x bin/linux/smews.elf ]
	    then
		fail $1 $2 "LAUNCH: binary not present or not executable"
		return 1
	    fi
	    sudo bin/linux/smews.elf &
	    ;;
	*)
	    fail $1 $2 "LAUNCH: target not supported by script"
	    return 1
	    ;;
    esac
 #   sleep 1
    return 0
}
