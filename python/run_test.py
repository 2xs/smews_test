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
        return True
    except smews.SmewsError as e:
        test.fail(e.message)
    return False
#####################################################


def test_program(test_suite, build_options):
    what = "program(test_suite: {} -- {})".format(test_suite, smews.build_options_to_string(build_options))
    test.begin(build_options["target"], what)
    try:
        smews.program(build_options["target"])
        test.success()
        return True
    except smews.SmewsError as e:
        test.fail(e.message)
    return False

def test_run(test_suite, build_options):
    what = "run(test_suite: {} -- {})".format(test_suite, smews.build_options_to_string(build_options))
    test.begin(build_options["target"], what)
    try:
        smews.run(build_options["target"])
        test.success()
        return True
    except smews.SmewsError as e:
        test.fail(e.message)
    return False

def do_test(test_script, test_suite, build_options):
    what = "test(test_suite: {} -- {} -- {}".format(test_suite, os.path.basename(test_script), smews.build_options_to_string(build_options))
    test.begin(build_options["target"], what)
    try:
        args = [test_script, build_options["ipaddr"]]
        system.execute(args)
        test.success()
        return True
    except system.ExecutionError as e:
        test.fail(e.message)
    return False

def do_tests(test_suite, build_options):
    # Get script to execute
    tests = test_suites.get_tests(test_suite, build_options["target"])
    for test in tests:
        do_test(test, test_suite, build_options)

def test_kill(test_suite, build_options):
    what = "kill(test_suite: {} -- {})".format(test_suite, smews.build_options_to_string(build_options))
    test.begin(build_options["target"], what)
    try:
        smews.kill(build_options["target"])
        test.success()
        return True
    except smews.SmewsError as e:
        test.fail(e.message)
    return False



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
        # Copy needed apps to smews folder
        test_suites.copy_apps(test_suite)
        disable_list = test_suites.get_disable_list(test_suite)
        build_options = {}
        for target in targets:
            build_options["target"] = target
            for ip in ips:
                build_options["ipaddr"] = ip
                for disable in disable_list:
                    build_options["disable"] = ",".join(disable)
                    build_options["apps"] = ",".join(apps)
                    # Build smews
                    if test_build(test_suite, build_options):
                        # Flash to device
                        if test_program(test_suite, build_options):
                            # Run smews
                            if test_run(test_suite, build_options):
                                # Executes tests
                                do_tests(test_suite, build_options)
                                # Kill
                                test_kill(test_suite, build_options)
        # Clean smews folder
        test_suites.remove_apps(test_suite)

except KeyboardInterrupt:
    sys.stderr.write("\nAbording tests\n")
finally:
    test.report(False)
