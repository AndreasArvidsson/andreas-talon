from talon import Context, Module
import subprocess

mod = Module()
mod.list("launch_command", desc="List of applications to launch")

ctx = Context()
ctx.lists["self.launch_command"] = {}

child_processes = []


@mod.action_class
class Actions:
    def exec(command: str):
        """Execute command"""
        # Store child process handle to avoid log warning about subprocess still running
        child_processes.append(
            subprocess.Popen(command, shell=True),
        )

    def system_shutdown():
        """Shutdown operating system"""

    def system_restart():
        """Restart operating system"""

    def system_hibernate():
        """Hibernate operating system"""

    def system_lock():
        """Lock operating system"""

    def app_switcher():
        """Show system application switcher"""
