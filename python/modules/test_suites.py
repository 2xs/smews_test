import os
from . import smews
from . import system

folder = "."

def get_list():
    global folder
    return system.get_subfolder_list(folder)
#####################################################    

def get_folder(test_suite):
    global folder
    test_suite_folder = os.path.join(folder, test_suite)
    return test_suite_folder
####################################################


def get_targets_to_test(test_suite):
    test_suite_folder = get_folder(test_suite)

    # target and notarget files
    target_file = os.path.join(test_suite_folder, "target")
    notarget_file = os.path.join(test_suite_folder, "notarget")

    # targets set
    smews_targets = set(smews.get_target_list())
    only_target_list = set(system.get_file_lines(target_file))
    no_target_list = set(system.get_file_lines(notarget_file))
    if len(only_target_list):
        return list((smews_targets & only_target_list) - no_target_list)
    else:
        return list(smews_targets - no_target_list)
####################################################        

def get_apps_to_include(test_suite):
    test_suite_folder = get_folder(test_suite)
    apps_file = os.path.join(test_suite_folder, "useapps")
    apps_path = os.path.join(test_suite_folder, "apps")
    provided_apps = set(system.get_subfolder_list(apps_path))
    apps = set(system.get_file_lines(apps_file))
    smews_apps = set(smews.get_apps())
    return list(provided_apps | (apps & smews_apps))
####################################################

def get_disable_list(test_suite):
    test_suite_folder = get_folder(test_suite)
    # files
    disable_file = os.path.join(test_suite_folder, "disable")
    nodisable_file = os.path.join(test_suite_folder, "nodisable")

    # sets
    smews_options = set(smews.get_disable_options())
    disable_options = set(system.get_file_lines(disable_file))
    nodisable_options = set(system.get_file_lines(nodisable_file))

    if len(disable_options):
        final_options_set = (smews_options & disable_options) - nodisable_options
    else:
        final_options_set = (smews_options) - nodisable_options
    combinations = get_options_combinations(list(final_options_set))
    combinations.append("")
    return combinations
####################################################

def get_options_combinations(options_list):
    if not options_list:
        return []
    if len(options_list) == 0:
        return []
    if len(options_list) == 1:
        return options_list
    if len(options_list) == 2:
        return [[options_list[0]],[options_list[1]], options_list]
    combinations = [[options_list[0]]]
    sub_comb = get_options_combinations(options_list[1:])
    for comb in  sub_comb:
        combinations.append(comb[:])
        comb.append(options_list[0])
        combinations.append(comb[:])
    return combinations    
#####################################################
