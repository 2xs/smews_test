#!/usr/bin/env python3

import sys, os, stat, subprocess


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
        sys.stdout.write("{}/{} tests passed ({:.2f} %)\n".format(success, len(Test.__tests), success / len(Test.__tests) * 100))
#####################################################

def chdir(path):
    current_path = os.getcwd()
    os.chdir(path)
    return current_path
#####################################################    

def get_target_list():
    global smews_folder
    targets_folder = os.path.join(smews_folder,"targets")
    targets = os.listdir(targets_folder)
    for target in targets[:]:
        file_path = os.path.join(targets_folder,target)
        mode = os.stat(file_path).st_mode
        if not stat.S_ISDIR(mode):
            targets.remove(target)
    return targets
#####################################################    

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



if len(sys.argv) < 2:
    sys.stderr.write("Usage: {0} <smews_folder>\n".format(sys.argv[0]))
    sys.exit(1)
else:
    smews_folder = sys.argv[1]

targets=get_target_list()
ips = ["192.168.100.200", "fc23::2"]

for target in targets:
    for ip in ips:
        Test.begin(target, "build({})".format(ip))
        try:
            perform_build({"ipaddr": ip, "target": target})
            Test.success()
        except:
            Test.fail()

Test.report()
