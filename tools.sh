#!/bin/bash

# Kill smews and exit
# args: $1 ip $2 target $3 value
function clean_exit()
{
    kill_smews $1 $2
    exit $3
}

# Kill smews
# return true if smews was running and false if not
# args: $1 ip, $2 target
function kill_smews()
{
    if ! [ $2 = "linux" ]
    then
	return 0
    fi
    if ! is_alive $1 $2
    then
	return 1
    fi
    while is_alive $1 $2
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

# Checks if smews is still alive
# args: $1 ip, $2 target
function is_alive()
{
    case $2 in
	linux)
	    pgrep smews.elf > /dev/null
	    return $?
	    ;;
	*)
	    ;;
    esac
    return 0
}

function flash_mbed()
{
    FOLDER=`mount | grep '/MBED ' | awk '{ print $3}'`
    if ! cp bin/mbed_ethernet/smews.bin $FOLDER
    then
	fail $1 $2 "Build: Failed to program MBED"
	return 1
    fi
    sync
    sleep 1
    # Reset MBED
    reset_mbed
    sleep 3 # Wait for flash
}

function reset_mbed()
{
    $TESTS_FOLDER/send_break /dev/ttyACM0
    sleep 3
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
    case $2 in
	mbed_ethernet)
	    flash_mbed
	    ;;
	*)
	    ;;
    esac
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
	mbed_ethernet)
	    # Reset MBED
	    reset_mbed
	    ;;
	*)
	    fail $1 $2 "LAUNCH: target not supported by script"
	    return 1
	    ;;
    esac
 #   sleep 1
    return 0
}

# returns true if $1 is a ipv6 addr
# Only check if a ':' character is present, so only works because the script calls it correctly
function is_v6()
{
    echo "$1" | grep -q ':'
}
