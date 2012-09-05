import subprocess
import os,sys
import stat
import fileinput

logfile = "error.log"

class SystemError(Exception):
    def __init__(self, message):
        self.message = message

class ExecutionError(SystemError):
    def __init__(self, message):
        self.message = "Execution Error: {}".format(message)

def execute(args):
    global logfile
    try:
        errorlog = open(logfile, "a+")
        devnull = open(os.devnull,"a+")
        errorlog.write("##################### Execution of {} ######################\n".format(args))
        errorlog.flush()
    except IOError:
        errorlog = open(os.devnull, "a+")
    try:
        subprocess.check_call(args, stdout=devnull, stderr=errorlog)
    except subprocess.CalledProcessError as e:
        raise ExecutionError("{} returned {}".format(args, e.returncode))
    except OSError:
        raise ExecutionError("failed to execute process: {}".format(args))

def chdir(path):
    current_path = os.getcwd()
    os.chdir(path)
    return current_path
#####################################################    


def create_logfile(lfile):
    global logfile
    logfile = lfile
    try:
        log = open(logfile,"w")
        log.close()
    except IOError:
        sys.stderr.write("Failed to create {}\n".format(logfile))


def get_executable_list(folder):
    try:
        files = os.listdir(folder)
        for entry in files[:]:
            file_path = os.path.join(folder,entry)
            if not os.access(file_path, os.X_OK):
                files.remove(entry)
                continue
            mode = os.stat(file_path).st_mode
            if stat.S_ISDIR(mode):
                files.remove(entry)
        files.sort()
        return files
    except OSError:
        return []
    

def get_subfolder_list(folder):
    try:
        subfolders = os.listdir(folder)
        for subfolder in subfolders[:]:
            file_path = os.path.join(folder,subfolder)
            mode = os.stat(file_path).st_mode
            if not stat.S_ISDIR(mode):
                subfolders.remove(subfolder)
        subfolders.sort()
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


def import_module(path, module):
    sys.path.append(path)
    mod = __import__(module)
    sys.path.remove(path)
    return mod

def unload_module(module):
    del(sys.modules[module])

