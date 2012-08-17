import os
from . import smews
from . import system

folder = "."
only = []

def get_list():
    global folder
    suites = system.get_subfolder_list(folder)
    suites.sort()
    return suites
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

def get_provided_apps(test_suite):
    test_suite_folder = get_folder(test_suite)
    apps_path = os.path.join(test_suite_folder, "apps")
    return system.get_subfolder_list(apps_path)
    

def get_apps_to_include(test_suite):
    test_suite_folder = get_folder(test_suite)
    apps_file = os.path.join(test_suite_folder, "useapps")
    provided_apps = set(get_provided_apps(test_suite))
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

def copy_apps(test_suite):
    provided_apps = get_provided_apps(test_suite)
    apps_path = os.path.join(get_folder(test_suite),"apps")
    smews_apps_folder = smews.get_apps_folder()
    for app in provided_apps:
        app_path = os.path.join(apps_path, app)
        args = ["cp", "-r", app_path, smews_apps_folder]
        system.execute(args)

def remove_apps(test_suite):
    provided_apps = get_provided_apps(test_suite)
    smews_apps_folder = smews.get_apps_folder()
    for app in provided_apps:
        smews_app_path = os.path.join(smews_apps_folder, app)
        args = ["rm", "-rf", smews_app_path]
        system.execute(args)

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

def get_tests(test_suite, target):
    global only
    test_suite_folder = get_folder(test_suite)
    tests_path = os.path.join(test_suite_folder, "tests")
    target_specific_tests_path = os.path.join(tests_path,"targets",target)
    tests = []
    test_scripts = system.get_executable_list(tests_path)
    target_specific_scripts = system.get_executable_list(target_specific_tests_path)
    if len(only):
        test_scripts = list(set(test_scripts) & set(only))
        target_specific_scripts = list(set(target_specific_scripts) & set(only))
    for test in test_scripts:
        tests.append(os.path.join(tests_path, test))
    for test in target_specific_scripts:
        tests.append(os.path.join(target_specific_tests_path, test))
    return tests
