#!/usr/bin/env python3

import sys, os
from modules import *

TEST_SUITES_FOLDER="test_suites"


def test_build(test_suite, build_options):
    what = "build(test_suite: {} -- {})".format(test_suite, smews.build_options_to_string(build_options))
    test.begin(build_options["target"], what)
    try:
        smews.build(build_options)
        test.success()
    except smews.SmewsError as e:
        test.fail(e.message)
#####################################################


def test_program(test_suite, build_options):
    what = "program(test_suite: {} -- {})".format(test_suite, smews.build_options_to_string(build_options))
    test.begin(build_options["target"], what)
    try:
        smews.program(build_options["target"])
        test.success()
    except smews.SmewsError as e:
        test.fail(e.message)

def test_run(test_suite, build_options):
    what = "run(test_suite: {} -- {})".format(test_suite, smews.build_options_to_string(build_options))
    test.begin(build_options["target"], what)
    try:
        smews.run(build_options["target"])
        test.success()
    except smews.SmewsError as e:
        test.fail(e.message)

def do_tests(test_suite, build_options):
    pass

def test_kill(test_suite, build_options):
    pass

if len(sys.argv) < 2:
    sys.stderr.write("Usage: {0} <smews_folder> [target1 ... targetN]\n".format(sys.argv[0]))
    sys.exit(1)

# Set needed folder to absolute paths
script_folder = os.path.abspath(sys.path[0])
smews.folder = os.path.abspath(sys.argv[1])
smews.tools_folder = os.path.join(script_folder, "tools")
# update the PATH environment so that all run scripts have a direct access to the tools scripts
os.environ["PATH"] = os.environ["PATH"] + ":" + smews.tools_folder


targets_to_test = sys.argv[2:]
test_suites.folder = os.path.join(script_folder, "test_suites")

ips = ["192.168.100.200", "fc23::2"]

try:
    test_suites_list = test_suites.get_list()
    for test_suite in test_suites_list:
        targets = test_suites.get_targets_to_test(test_suite)
        if targets_to_test and len(targets_to_test):
            targets = list(set(targets) & set(targets_to_test))
        apps = test_suites.get_apps_to_include(test_suite)
        disable_list = test_suites.get_disable_list(test_suite)
        build_options = {}
        for target in targets:
            build_options["target"] = target
            for ip in ips:
                build_options["ipaddr"] = ip
                for disable in disable_list:
                    build_options["disable"] = ",".join(disable)
                    # Build smews
                    test_build(test_suite, build_options)
                    # Flash to device
                    test_program(test_suite, build_options)
                    # Run smews
                    test_run(test_suite, build_options)
                    # Executes tests
                    do_tests(test_suite, build_options)
                    # Kill
                    test_kill(test_suite, build_options)

except KeyboardInterrupt:
    sys.stderr.write("\nAbording tests\n")
finally:
    test.report(True)
