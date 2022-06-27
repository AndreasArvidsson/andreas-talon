from talon import Context, Module

mod = Module()
ctx = Context()


@mod.capture(rule="dot {user.extension}")
def extension(m) -> str:
    return f".{m.extension}"


@mod.capture(rule="dot {user.domain}")
def domain(m) -> str:
    return f".{m.domain}"


# fmt: off

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
    "java":           "java",
    "java script":    "js",
    "type script":    "ts",
    "text":           "txt",
    "lua":            "lua",
    "csv":            "csv",
    "xml":            "xml",
    "html":           "html",
}

mod.list("domain", desc="List of top level domains")
ctx.lists["self.domain"] = {
    "com":            "com",
    "net":            "net",
    "org":            "org",
    "sweden":         "se",
}

extension_siblings = {
    "talon":        "py",
    "py":           "talon",
    "c":            "h",
    "cpp":          "h",
    "h":            "c",
    "tsx":          "ts",
    "jsx":          "js",
    "ts":           "tsx",
    "js":           "jsx",
}

# fmt: on

@mod.action_class
class UserActions:
    def get_extension_sibling(extension: str) -> str:
        """Get matching sibling for extension"""
        if extension in extension_siblings:
            return extension_siblings[extension]
        return None