#!/usr/bin/env python3

import sys, os, stat, subprocess
import fileinput

TEST_SUITES_FOLDER="test_suites"

class Test:
    __tests = []
    def begin(target, what):
        Test.__tests.append({"target": target, "what": what, "success": False})
    def success():
        Test.__tests[len(Test.__tests)-1]["success"] = True
        sys.stdout.write(".")
        sys.stdout.flush()
    def fail():
        sys.stdout.write("X")
        sys.stdout.flush()
    def report():
        print("")
        success = 0
        for test in Test.__tests:
            if not test["success"]:
                sys.stderr.write("FAIL({}): {}\n".format(test["target"], test["what"]))
            else:
                success = success + 1
        if not len(Test.__tests):
            print("No test performed")
        else:
            print("{}/{} tests passed ({:.2f} %)".format(success, len(Test.__tests), success / len(Test.__tests) * 100))
#####################################################

def chdir(path):
    current_path = os.getcwd()
    os.chdir(path)
    return current_path
#####################################################    

def get_subfolder_list(folder):
    try:
        subfolders = os.listdir(folder)
        for subfolder in subfolders[:]:
            file_path = os.path.join(folder,subfolder)
            mode = os.stat(file_path).st_mode
            if not stat.S_ISDIR(mode):
                subfolders.remove(subfolder)
        return subfolders
    except:
        return []
####################################################

def get_smews_target_list():
    global smews_folder
    targets_folder = os.path.join(smews_folder,"targets")
    return get_subfolder_list(targets_folder)
#####################################################    

def get_test_suite_list():
    global script_folder
    global TEST_SUITES_FOLDER
    test_suite_folder = os.path.join(script_folder, TEST_SUITES_FOLDER);
    return get_subfolder_list(test_suite_folder)

def execute_command(args):
    process = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    while not process.poll():
        try:
            process.communicate()
        except:
            break
    if process.returncode:
        raise subprocess.CalledProcessError(process.returncode, args)
#####################################################

def perform_build(build_options):
    global smews_folder
    args = ["scons", "-c"]
    test_path = chdir(smews_folder)
    subprocess.check_output(args)
    args = ["scons"]
    for (option,value) in build_options.items():
        args.append("{}={}".format(option,value))
    try:
        execute_command(args)
    except:
        chdir(test_path)
        raise
    chdir(test_path)
#####################################################

def test_target(target, ip):
        Test.begin(target, "build({})".format(ip))
        try:
            perform_build({"ipaddr": ip, "target": target})
            Test.success()
        except:
            Test.fail()
#####################################################

def get_file_lines(file_path):
    try:
        lines = []
        f = fileinput.input(files=(file_path))
        for line in f:
            lines.append(line[:-1])
        f.close()
        return lines
    except AttributeError as e:
        print(e)
        return []
    except:
        return []
####################################################
    
def get_test_suite_folder(test_suite):
    global script_folder, TEST_SUITES_FOLDER
    test_suite_folder = os.path.join(os.path.join(script_folder, TEST_SUITES_FOLDER), test_suite)
    return test_suite_folder
####################################################


def get_targets_to_test(test_suite):
    test_suite_folder = get_test_suite_folder(test_suite)

    # target and notarget files
    target_file = os.path.join(test_suite_folder, "target")
    notarget_file = os.path.join(test_suite_folder, "notarget")

    # targets set
    smews_targets = set(get_smews_target_list())
    only_target_list = set(get_file_lines(target_file))
    no_target_list = set(get_file_lines(notarget_file))
    if len(only_target_list):
        return list((smews_targets & only_target_list) - no_target_list)
    else:
        return list(smews_targets - no_target_list)
####################################################        

def get_apps_to_include(test_suite):
    global smews_folder
    test_suite_folder = get_test_suite_folder(test_suite)
    apps_file = os.path.join(test_suite_folder, "useapps")
    apps_path = os.path.join(test_suite_folder, "apps")
    provided_apps = set(get_subfolder_list(apps_path))
    apps = set(get_file_lines(apps_file))
    smews_apps = set(get_subfolder_list(os.path.join(smews_folder, "apps")))
    return list(provided_apps | (apps & smews_apps))
####################################################

def get_smews_disable_options():
    global smews_folder
    return ['comet', 'post', 'timers', 'arguments', 'general_purpose_ip_handler']

def get_disable_list(test_suite):
    test_suite_folder = get_test_suite_folder(test_suite)
    # files
    disable_file = os.path.join(test_suite_folder, "disable")
    nodisable_file = os.path.join(test_suite_folder, "nodisable")

    # sets
    smews_options = set(get_smews_disable_options())
    disable_options = set(get_file_lines(disable_file))
    nodisable_options = set(get_file_lines(nodisable_file))

    if len(disable_options):
        final_options_set = (smews_options & disable_options) - nodisable_options
    else:
        final_options_set = (smews_options) - nodisable_options
    print(list(final_options_set))
    return list(final_options_set)
####################################################

if len(sys.argv) < 2:
    sys.stderr.write("Usage: {0} <smews_folder>\n".format(sys.argv[0]))
    sys.exit(1)
else:
    smews_folder = sys.argv[1]

script_folder = sys.path[0]

targets=get_smews_target_list()
ips = ["192.168.100.200", "fc23::2"]

test_suites = get_test_suite_list()
for test_suite in test_suites:
    print(test_suite)
    print("targets: {}".format(get_targets_to_test(test_suite)))
    print("apps: {}".format(get_apps_to_include(test_suite)))
    print("disable: {}".format(get_disable_list(test_suite)))
    

# for target in targets:
#     for ip in ips:
#         test_target(target, ip)

Test.report()
