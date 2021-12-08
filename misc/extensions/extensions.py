from talon import Context, Module

mod = Module()
ctx = Context()


mod.list("extension", desc="List of file extensions")
ctx.lists["self.extension"] = {
    "pie":            "py",
    "talon":          "talon",
    "mark down":      "md",
    "shell":          "sh",
    "vim":            "vim",
    "see":            "c",
    "see sharp":      "cs",
    "see plus plus":  "cpp",
    "exe":            "exe",
    "bin":            "bin",
    "jason":          "json",
    "jay son":        "json",
    "java":           "java",
    "java script":    "js",
    "type script":    "ts",
    "text":           "txt",
    "lua":            "lua"
}

@mod.capture(rule="dot {user.extension}")
def extension(m) -> str:
    return f".{m.extension}"


mod.list("domain", desc="List of top level domains")
ctx.lists["self.domain"] = {
    "com":            "com",
    "net":            "net",
    "org":            "org",
    "sweden":         "se"
}

@mod.capture(rule="dot {user.domain}")
def domain(m) -> str:
    return f".{m.domain}"