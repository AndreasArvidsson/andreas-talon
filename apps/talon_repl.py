from talon import Module

mod = Module()

mod.apps.talon_repl = r"""
os: windows
and app.exe: cmd.exe
os: windows
and app.exe: conhost.exe
os: windows
and app.exe: windowsterminal.exe

title: Talon - REPL
"""
