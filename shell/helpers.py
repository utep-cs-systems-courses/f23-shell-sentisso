import os, sys
import command

STDERR = sys.stderr.fileno()
STDOUT = sys.stdout.fileno()
STDIN = sys.stdin.fileno()
BUILT_IN_COMMANDS = ["cd", "exit"]
PS1 = os.environ.get("PS1", "$ ")
pid = os.getpid()


def print_prompt():
    print(PS1, end="")


def read_prompt():
    try:
        return input()
    except EOFError:
        sys.exit(1)


def process_prompt(prompt: str):
    prompt.strip()
    if len(prompt) == 0:
        return
    pipes = prompt.split("|")
    pipe_r = None
    pipe_w = None

    os.write(2, (f"prompt: {prompt}\n").encode())

    for index, cmd in enumerate(pipes):
        args = cmd.split()

        if index < len(pipes) - 1:
            pipe_w = os.pipe()  # (r, w)
            for fd in pipe_w:
                os.set_inheritable(fd, True)
        else:  # if last process, do not redirect output
            pipe_w = None

        if command.process_builtin(args):
            continue  # this command was built-in

        rc = os.fork()
        if rc == 0:  # child
            if pipe_r is not None:
                # redirect child's stdin to pipe_r
                os.dup2(pipe_r[0], STDIN)
                for fd in pipe_r:
                    os.close(fd)

            if pipe_w is not None:
                # redirect child's stdout to pipe_w
                os.dup2(pipe_w[1], STDOUT)
                for fd in pipe_w:
                    os.close(fd)

            command.process(args)

        elif rc > 0:  # parent
            if pipe_r:
                os.close(pipe_r[0])
                os.close(pipe_r[1])
            pipe_r = pipe_w  # next process reads from this process's output
            (pid, exit_code) = os.wait()
            if exit_code != 0:
                os.write(STDOUT, ("Program terminated with exit code %d\n" % exit_code).encode())

        else:
            os.write(STDERR, ("fork failed, returning %d\n" % rc).encode())
            sys.exit(1)
