from talon import Module, Context

mod = Module()
ctx = Context()

mod.list("swedish_phrase", desc="List of Swedish phrases")
ctx.lists["self.swedish_phrase"] = {
    "hello": "Hej",
    "goodbye": "Hejdå",
    "thanks": "Tack",
}
