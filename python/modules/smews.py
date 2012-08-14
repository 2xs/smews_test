import os
from . import system

class SmewsError(Exception):
    pass

class SmewsProgramError(SmewsError):
    def __init__(self, message):
        self.message = message

class SmewsBuildError(SmewsError):
    def __init__(self, message):
        self.message = message

class SmewsRunError(SmewsError):
    def __init__(self, message):
        self.message = message

folder = "."
tools_folder = "."

def build_options_to_string(build_options):
    str = ""
    for (option,value) in build_options.items():
        str = str + " {}={}".format(option,value)
    return str
    

def build(build_options):
    global folder
    try:
        args = ["scons", "-c"]
        test_path = system.chdir(folder)
        system.execute(args)
        args = ["scons"]
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

def get_apps():
    global folder
    return system.get_subfolder_list(os.path.join(folder, "apps"))

def program(target):
    global folder
    global tools_folder
    program_script = os.path.join(os.path.join(tools_folder,target),"program")
    args = [program_script, folder]
    try:
        system.execute(args)
    except system.ExecutionError as e:
        raise SmewsProgramError(e.message)


def run(target):
    global folder
    global tools_folder
    run_script = os.path.join(os.path.join(tools_folder,target),"run")
    args = [run_script, folder]
    try:
        system.execute(args)
    except system.ExecutionError as e:
        raise SmewsRunError(e.message)
    
