import os, sys, time, re
from typing import List
import redirect

BUILT_IN_COMMANDS = ["cd", "exit"]


def process_builtin(args: List[str]):
    """
    Check if the given command is a built-in command and process it if it is.
    :param args: the list of arguments
    :return: True if the command was a built-in command, False otherwise.
    """
    if args[0] == "exit":
        sys.exit(0)
        return True

    elif args[0] == "cd":
        try:
            os.chdir(args[1])
        except FileNotFoundError:
            os.write(2, ("cd: %s: No such file or directory\n" % args[1]).encode())

        return True

    return False


def process(args: List[str]):
    """
    Process the given non-built-in command with args.
    It is expected that this function is already called within a child process.
    :return: None
    """
    args = redirect.stdout(args)
    args = redirect.stdin(args)

    for path in re.split(":", os.environ['PATH']):  # try each directory in path
        if args[0][0] != "/":
            path = "%s/%s" % (path, args[0])
        else:
            path = args[0]
        try:
            os.execve(path, args, os.environ)  # try to exec program
            # os.exec* replaces the current process with the new process
            # therefore that process termination will exit for us
        except FileNotFoundError:
            pass

    # we did not find the command in any of the paths
    os.write(2, ("%s: command not found\n" % args[0]).encode())
    sys.exit(1)
