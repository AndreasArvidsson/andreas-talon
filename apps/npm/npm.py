from talon import Module, Context

mod = Module()
ctx = Context()

mod.tag("npm")

mod.list("npm_command", desc="List of npm commands")
mod.list("pnpm_command", desc="List of pnpm commands")
mod.list("gss_module", desc="List of gss modules")

npm_commands = {
    "version": "-v\n",
    "init": "init ",
    "install": "install ",
    "install global": "install -g ",
    "uninstall": "uninstall ",
    "uninstall global": "uninstall -g ",
    "link": "link ",
    "list": "list\n",
    "list global": "list -g\n",
    "outdated": "outdated\n",
    "why": "why ",
    "y": "why ",
    "update": "update --save ",
    "prune": "prune\n",
    "dedupe": "dedupe\n",
    "audit": "audit\n",
    "publish": "publish --dry-run",
    "start": "start\n",
    "build": "build\n",
    "test": "test\n",
    "run": "run ",
    "clean": "run clean\n",
    "run build": "run build\n",
    "run build watch": "run build:watch\n",
}


ctx.lists["user.npm_command"] = npm_commands

ctx.lists["user.pnpm_command"] = {
    **npm_commands,
    "outdated": "outdated -r\n",
    "why": "why -r ",
    "y": "why -r ",
    "update": "update ",
}
