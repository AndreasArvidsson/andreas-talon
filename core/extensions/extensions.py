from talon import Context, Module, actions

mod = Module()
ctx = Context()


@mod.capture(rule="dot ({user.code_extension} | {user.file_extension})")
def extension(m) -> str:
    return f".{m[-1]}"


@mod.capture(rule="[{user.formatter_code}] <user.text> [<user.extension>]")
def filename(m) -> str:
    try:
        text = actions.user.format_text(m.text, m.formatter_code)
    except AttributeError:
        text = m.text
    try:
        extension = m.extension
    except AttributeError:
        extension = ""
    return f"{text}{extension}"


@mod.capture(rule="dot {user.domain}")
def domain(m) -> str:
    return f".{m.domain}"


# fmt: off

mod.list("file_extension", desc="List of (non-code) file extensions")
ctx.lists["self.file_extension"] = {
    "exe":            "exe",
    "bin":            "bin",
}

mod.list("domain", desc="List of top level domains")
ctx.lists["self.domain"] = {
    "com":            "com",
    "net":            "net",
    "org":            "org",
    "sweden":         "se",
    "s e":           "se",
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
