from talon import Context, Module, cron
import subprocess

mod = Module()
mod.list("launch_command", "List of applications to launch")

ctx = Context()
ctx.lists["user.launch_command"] = {}

child_processes = []


def remove_if_done(proc: subprocess.Popen):
    if proc.poll() is not None and proc in child_processes:
        child_processes.remove(proc)


@mod.action_class
class Actions:
    @staticmethod
    def exec(command: str):
        """Execute command"""
        # Store child process handle to avoid log warning about subprocess still running
        proc = subprocess.Popen(command, shell=True)
        child_processes.append(proc)
        cron.after("5s", lambda: remove_if_done(proc))

    def system_shutdown():
        """Shutdown operating system"""

    def system_restart():
        """Restart operating system"""

    def system_hibernate():
        """Hibernate operating system"""

    def system_lock():
        """Lock operating system"""
