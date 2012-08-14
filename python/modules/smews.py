import os
from . import system

folder = "."

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
