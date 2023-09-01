from talon import Module, Context

mod = Module()
ctx = Context()

mod.list("swedish_phrase", "List of Swedish phrases")
ctx.lists["self.swedish_phrase"] = {
    "hello": "Hej",
    "goodbye": "Hejdå",
    "thanks": "Tack",
    "cannon": "Kanon",
    "great": "Kanon",
    "correct": "Korrekt",
    "yes": "Ja",
    "no": "Nej",
    "done": "Klart",
}
