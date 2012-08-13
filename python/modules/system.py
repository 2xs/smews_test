import subprocess
import os
import stat
import fileinput

class SystemError(Exception):
    def __init__(self, message):
        self.message = message

class ExecutionError(SystemError):
    def __init__(self, message):
        self.message = "Execution Error: {}".format(message)

def execute(args):
    try:
        process = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except OSError:
        raise ExecutionError("Failed to execute process: {}".format(args))
    while not process.poll():
        try:
            process.communicate()
        except ValueError:
            break
    if process.returncode:
        raise ExecutionError("process returned {}".format(process.returncode))
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
    except OSError:
        return []
####################################################

def get_file_lines(file_path):
    try:
        lines = []
        f = fileinput.input(files=(file_path))
        for line in f:
            lines.append(line[:-1])
        f.close()
        return lines
    except AttributeError as e:
        return []
    except IOError:
        return []
####################################################
