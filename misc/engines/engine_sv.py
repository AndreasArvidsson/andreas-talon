from talon import Context, Module

mod = Module()
ctx = Context()
mod.tag("swedish")

ctx.matches = r"""
tag: user.swedish
"""

ctx.settings = {
    "speech.engine": "webspeech",
    "speech.language": "sv_SE",
}
