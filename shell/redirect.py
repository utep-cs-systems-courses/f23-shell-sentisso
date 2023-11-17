import os, sys
from typing import List


def stdout(args: List[str]):
    """
    Handle redirection of stdout if necessary.
    :param args: the list of arguments
    :return: the list of arguments with the redirection removed
    """
    try:
        ri = args.index(">")

        if len(args) > 2 and 0 < ri < len(args) - 1:  # if valid redirection
            # redirect stdout
            os.close(1)
            os.open(args[ri + 1], os.O_CREAT | os.O_WRONLY)
            os.set_inheritable(1, True)
            return args[:ri]

        else:  # invalid redirection
            os.write(2, "invalid redirection used\n".encode())
            sys.exit(1)

    except ValueError:
        return args


def stdin(args: List[str]):
    """
    Handle redirection of stdin if necessary.
    :param args: the list of arguments
    :return: the list of arguments with the redirection removed
    """
    try:
        ri = args.index("<")

        if len(args) > 2 and 0 < ri < len(args) - 1:  # if valid redirection
            # redirect stdin
            os.close(0)
            os.open(args[ri + 1], os.O_RDONLY)
            os.set_inheritable(0, True)
            return args[:ri]

        else:  # invalid redirection
            os.write(2, "invalid redirection used\n".encode())
            sys.exit(1)

    except ValueError:
        return args
