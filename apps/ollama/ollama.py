from talon import Module, Context

mod = Module()
ctx = Context()

mod.tag("ollama")
mod.list("ollama_model", desc="list of ollama models")

ctx.lists["user.ollama_model"] = {
    "gemma": "gemma2:2b",
    "llama": "llama3.1:8b",
}
