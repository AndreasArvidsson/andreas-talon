from talon import Module, Context

mod = Module()
ctx = Context()

mod.list("swedish_word", desc="List of Swedish words")
ctx.lists["self.swedish_word"] = {
    "hello": "Hej",
    "goodbye": "Hejdå",
    "thanks": "Tack",
}
