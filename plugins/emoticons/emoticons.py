from talon import Module, Context

mod = Module()
ctx = Context()

mod.list("emoticon", "List of emoticons")

ctx.lists["user.emoticon"] = {
    "smile": ":)",
    "grin": ":D",
    "wink": ";)",
    "tongue": ":p",
    "unsure": ":/",
    "gasp": ":o",
    "sad": ":(",
    "crying": ":'(",
}
