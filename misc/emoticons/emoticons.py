from talon import Module, Context

mod = Module()
ctx = Context()

mod.list("emoticon", desc="List of emoticons")

ctx.lists["self.emoticon"] = {
    "smile": ":)",
    "wink": ";)",
    "sad": ":(",
    "unsure": ":/",
    "grin": ":D",
    "gasp": ":o",
    "tongue": ":p",
}
