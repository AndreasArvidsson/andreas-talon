from talon import Module, actions

mod = Module()

mod.apps.youtube = """
tag: browser
browser.host: www.youtube.com
browser.path: /watch
"""
