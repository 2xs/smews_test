import os
from . import system

class SmewsError(Exception):
    pass


class SmewsBuildError(SmewsError):
    def __init__(self, message):
        self.message = message

class SmewsScriptError(SmewsError):
    def __init__(self, message, script):
        self.message = script + ": " + message

folder = "."
tools_folder = "."

def build_options_to_string(build_options):
    str = ""
    for (option,value) in build_options.items():
        str = str + "{}={} ".format(option,value)
    return str.strip()
    

def build(build_options):
    global folder
    try:
        args = ["scons", "-c", "-j10"]
        test_path = system.chdir(folder)
        system.execute(args)
        args = ["scons", "-j10"]
        for (option,value) in build_options.items():
            args.append("{}={}".format(option,value))
        system.execute(args)
    except system.ExecutionError as e:
        raise SmewsBuildError(e.message)
    finally:
        system.chdir(test_path)
#####################################################


def get_target_list():
    global folder
    targets_folder = os.path.join(folder,"targets")
    return system.get_subfolder_list(targets_folder)
#####################################################    


def get_disable_options():
    return ['comet', 'post', 'timers', 'arguments', 'general_purpose_ip_handler']
#####################################################    

def get_apps_folder():
    global folder
    return os.path.join(folder, "apps")

def get_apps():
    global folder
    return system.get_subfolder_list(get_apps_folder())

def run_script(target, script):
    global folder
    global tools_folder
    script = os.path.join(tools_folder,target,script)
    args = [script, folder]
    try:
        system.execute(args)
    except system.ExecutionError as e:
        raise SmewsScriptError(e.message, script)
    

def program(target):
    run_script(target, "program")

def run(target):
    run_script(target, "run")

def kill(target):
    run_script(target, "kill")
