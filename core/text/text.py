from talon import Module, Context

mod = Module()
ctx = Context()


mod.list("phrase_ender", desc="List of commands that can be used to end a phrase")
ctx.lists["self.phrase_ender"] = {
    "void": " ",
    "slap": "\n",
    "question": "?",
    "over": "",
}
