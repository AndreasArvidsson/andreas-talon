from talon import Context, Module

mod = Module()
ctx = Context()

mod.list("webpage", desc="List of webpages")

ctx.lists["self.webpage"] = {
    "github":               "https://github.com",
    "talon slack":          "https://talonvoice.slack.com",
    "regex cheat sheet":    "https://duckduckgo.com/?q=regex+cheat+sheet&t=ffab&ia=cheatsheet&iax=1",
    "avanza":               "https://www.avanza.se",
    "savr":                 "https://www.savr.com",
    "swedbank":             "https://swedbank.com",
    "sweclockers":          "https://www.sweclockers.com",
    "goodreads":            "https://www.goodreads.com"
}