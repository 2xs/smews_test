#!/usr/bin/env python3

import sys, os
from modules import *

TEST_SUITES_FOLDER="test_suites"


def test_build(test_suite, build_options):
    what = "build(test_suite: {} -- ip: {} -- ".format(test_suite, build_options["ipaddr"])
    if (build_options["disable"] == ""):
        what = what + "all options)"
    else:
        what = what + "disabled options: {})".format(build_options["disable"])
    test.begin(build_options["target"], what)
    try:
        smews.build(build_options)
        test.success()
    except system.ExecutionError as e:
        test.fail(e.message)
#####################################################


if len(sys.argv) < 2:
    sys.stderr.write("Usage: {0} <smews_folder> [target1 ... targetN]\n".format(sys.argv[0]))
    sys.exit(1)
else:
    smews.folder = sys.argv[1]
    targets_to_test = sys.argv[2:]

script_folder = sys.path[0]
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
                    test_build(test_suite, build_options)
                #execute_test_suite(test_suite, build_options)
except KeyboardInterrupt:
    sys.stderr.write("\nAbording tests\n")

test.report(True)
