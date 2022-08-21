from talon import Context, Module, actions, scope
from dataclasses import dataclass

mod = Module()
ctx = Context()


@dataclass
class Language:
    id: str
    extension: str
    spoken_form: str


languages = [
    Language("batch", "bat", "batch"),
    Language("c", "c", "see"),
    Language("cplusplus", "cpp", "see plus plus"),
    Language("csharp", "cs", "see sharp"),
    Language("csv", "csv", "csv"),
    Language("css", "css", "css"),
    Language("go", "go", "go"),
    Language("html", "html", "html"),
    Language("java", "java", "java"),
    Language("javascript", "js", "java script"),
    Language("javascriptreact", "jsx", "java script react"),
    Language("json", "json", "json"),
    Language("jsonl", "jsonl", "json lines"),
    Language("lua", "lua", "lua"),
    Language("markdown", "md", "mark down"),
    Language("perl", "pl", "perl"),
    Language("plaintext", "txt", "text"),
    Language("powershell", "ps1", "power shell"),
    Language("python", "py", "python"),
    Language("r", "r", "are"),
    Language("ruby", "rb", "ruby"),
    Language("shellscript", "sh", "shell script"),
    Language("talon", "talon", "talon"),
    Language("typescript", "ts", "type script"),
    Language("typescriptreact", "tsx", "type script react"),
    Language("xml", "xml", "xml"),
]

mod.list("code_extension", desc="List of file programming languages file extensions")
ctx.lists["self.code_extension"] = {
    **{l.spoken_form: l.extension for l in languages},
    "pie": "py",
}

mod.list("code_language", desc="List of file programming language identifiers")
ctx.lists["self.code_language"] = {l.spoken_form: l.id for l in languages}

extension_lang_map = {
    **{f".{l.extension}": l.id for l in languages},
    ".bashbook": "bash",
    ".ipynb": "python",
    ".h": "c",
}

language_ids = {l.id for l in languages}

# Create a context for each defined language
for lang in extension_lang_map.values():
    mod.tag(lang)
    mod.tag(f"{lang}_forced")
    c = Context()
    # Context is active if language is forced or auto language matches
    c.matches = f"""
    tag: user.{lang}_forced
    tag: user.auto_lang
    and code.language: {lang}
    """
    c.tags = [f"user.{lang}"]

# Create a mode for the automated language detection. This is active when no lang is forced.
mod.tag("auto_lang")
ctx.tags = ["user.auto_lang"]


@ctx.action_class("code")
class CodeActions:
    def language() -> str:
        file_extension = actions.win.file_ext()
        if file_extension in extension_lang_map:
            return extension_lang_map[file_extension]
        return ""


ctx_auto = Context()
ctx_auto.matches = r"""
tag: user.auto_lang
"""


@ctx_auto.action_class("user")
class AutoUserActions:
    def code_language():
        return actions.code.language()


@mod.action_class
class Actions:
    def code_set_language_mode(language: str):
        """Sets the active language mode, and disables extension matching"""
        ctx.tags = [f"user.{language}_forced"]
        actions.user.notify(f"Enabled {language} mode")

    def code_clear_language_mode():
        """Clears the active language mode, and re-enables code.language: extension matching"""
        ctx.tags = ["user.auto_lang"]

    def code_language() -> str:
        """Get the active language mode"""
        for tag in scope.get("tag"):
            lang = tag[5:]
            if lang in language_ids:
                return lang
        return ""
