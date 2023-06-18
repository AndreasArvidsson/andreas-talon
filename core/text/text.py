from talon import Module, Context

mod = Module()
ctx = Context()


mod.list("phrase_ender", desc="List of commands that can be used to end a phrase")
ctx.lists["self.phrase_ender"] = {
    "over": "",
    "question": "?",
    "slap": "\n",
    "spam": ", ",
    "void": " ",
}
