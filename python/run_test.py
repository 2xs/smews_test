#!/usr/bin/env python3

import sys, os, stat, subprocess


def chdir(path):
    current_path = os.getcwd()
    os.chdir(path)
    return current_path
######################################################    

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
######################################################    

def execute_command(args):
    process = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    while not process.poll():
        try:
            process.communicate()
        except:
            break
    if process.returncode:
        raise subprocess.CalledProcessError(process.returncode, args)
######################################################

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
########################################################



if len(sys.argv) < 2:
    sys.stderr.write("Usage: {0} <smews_folder>\n".format(sys.argv[0]))
else:
    smews_folder = sys.argv[1]

targets=get_target_list()

current_target=""
for target in targets:
    current_target = target
    try:
        print("Performing build for target {}".format(target))
        perform_build({"ipaddr": "192.168.100.200", "target": target})
    except OSError as e:
        sys.stderr.write("Build of target {} failed: {}\n".format(current_target, e))
    except subprocess.CalledProcessError as e:
        sys.stderr.write("Build of target {} failed: {}\n".format(current_target, e))
