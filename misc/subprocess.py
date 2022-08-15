from talon import Module, cron, actions
from typing import Optional
import subprocess
import os

mod = Module()
procs = []
IGNORE_PATTERNS = []


@mod.action_class
class Actions:
    def test():
        """"""
        print(actions.user.execparen(["node", "~/test.js"], verbose=False))
        # actions.user.execnbparen(["node", "~/test.js"])

    def execparen(
        cmd: list[str],
        cwd: Optional[str] = None,
        env: Optional[dict] = None,
        verbose: bool = True,
    ):
        """execute a command on the system, printing the output"""
        cmd = [os.path.expanduser(str(s)) for s in cmd]

        env_ = env_for_subprocess()
        if env is not None:
            env_ = env_ | env

        proc = subprocess.Popen(
            cmd,
            cwd=cwd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env=env_,
        )
        proc.wait()
        exit_code = proc.returncode
        stdout, stderr = consume_process_output(proc, verbose)

        return stdout, stderr, exit_code

    def execnbparen(
        cmd: list[str],
        cwd: Optional[str] = None,
        env: Optional[dict] = None,
        quiet: bool = True,
    ):
        """execute a command on the system, printing the output"""
        global procs

        cmd = [os.path.expanduser(str(s)) for s in cmd]

        if not quiet:
            print(f"executing asynchronously: {cmd}")

        env_ = env_for_subprocess()
        if env is not None:
            env_ = env_ | env

        proc = subprocess.Popen(
            cmd,
            cwd=cwd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env=env_,
        )

        # add it to the list to be raeaped when it finishes. We must do this or it will be become a zombie.
        procs.append(proc)


def env_for_subprocess():
    """returns the environment dictionary to be used for subprocesses"""
    path_components = [
        # os.path.expanduser("~/bin/pc"),
        # os.path.expanduser("~/bin/vendor"),
        # os.path.expanduser("~/homebrew-bin"),
        # os.path.expanduser("~/.pyenv/shims"),
        os.getenv("PATH"),
    ]
    env = os.environ.copy()
    env.update(
        {
            "PATH": ":".join(path_components),
        }
    )
    return env


def consume_process_output(proc: any, print_out: bool):
    """returns the processes' stdout/stderr, optionally prints it to the terminal"""
    stdout, stderr = proc.communicate()

    stdout = stdout.decode("utf-8").strip()
    stderr = stderr.decode("utf-8").strip()

    if print_out:
        print(f"{' '.join(proc.args)} exited with code {proc.returncode}:")
        for line in [l for l in stdout.split("\n") if len(l)]:
            print(f"[stdout] {line}")
        for line in [l for l in stderr.split("\n") if len(l)]:
            print(f"[stderr] {line}")

    if proc.stdout:
        proc.stdout.close()
    if proc.stderr:
        proc.stderr.close()

    return stdout, stderr


def cleanup_processes():
    """Cleans up asynchronous processes"""
    global procs

    new_procs = []

    for proc in procs:
        if proc.poll() is None:
            print(proc.pid, proc, proc.poll(), "still running, keep waiting")
            new_procs.append(proc)
            continue

        # Process finished, reap it.
        print(f"Reap process #{proc.pid} ({proc}) (finished!)")
        if proc.returncode != 0:
            if any([p not in " ".join(proc.args) for p in IGNORE_PATTERNS]):
                print(
                    f"Process \"{' '.join(proc.args)}\" returned exit code {proc.returncode}. (It's in IGNORE_PATTERNS, so we are not showing a notification)",
                )
            else:
                actions.user.notify(
                    f"Process returned exit code {proc.returncode}!",
                    " ".join(proc.args),
                )

        # consume_process_output(proc, proc.returncode != 0)
        res = consume_process_output(proc, proc.returncode != 0)
        print(res)

    procs = new_procs


cron.interval("1s", cleanup_processes)
