import sys

__tests = []

def begin(target, what):
    global __tests
    __tests.append({"target": target, "what": what, "success": False, "why": "Unknow reason"})

def success():
    global __tests
    __tests[len(__tests)-1]["success"] = True
    sys.stdout.write(".")
    sys.stdout.flush()

def fail(message=None):
    global __tests
    if message:
        __tests[len(__tests)-1]["why"] = message
    sys.stdout.write("X")
    sys.stdout.flush()


def report(full=False):
    global __tests
    print("")
    success = 0
    for test in __tests:
        if not test["success"]:
            sys.stderr.write("FAIL   ({}): {} - {}\n".format(test["target"], test["what"], test["why"]))
        else:
            if full:
                sys.stderr.write("SUCCESS({}): {}\n".format(test["target"], test["what"]))
            success = success + 1
    if not len(__tests):
        print("No test performed")
    else:
        print("{}/{} tests passed ({:.2f} %)".format(success, len(__tests), success / len(__tests) * 100))
#####################################################
