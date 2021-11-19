from talon import Context, Module
import os


mod = Module()
mod.list("launch_command", desc="List of applications to launch")

ctx = Context()
ctx.lists["self.launch_command"] = {}


@mod.action_class
class Actions:
    def exec(command: str):
        """Run command"""
        os.system(command)

    def system_shutdown():
        """Shutdown operating system"""

    def system_restart():
        """Restart operating system"""

    def system_hibernate():
        """Hibernate operating system"""
