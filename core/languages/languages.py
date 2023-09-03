from talon import Context, Module, actions
from dataclasses import dataclass


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
    Language("javascript", "mjs", "java script"),
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
    Language("scm", "scm", "tree sitter"),
    Language("snippet", "snippet", "snippet"),
    Language("talon", "talon", "talon"),
    Language("talon-list", "talon-list", "talon list"),
    Language("typescript", "ts", "type script"),
    Language("typescriptreact", "tsx", "type script react"),
    Language("xml", "xml", "xml"),
]

extension_lang_map = {
    **{f".{l.extension}": l.id for l in languages},
    ".bashbook": "bash",
    ".ipynb": "python",
    ".h": "c",
}

language_ids = set(extension_lang_map.values())
forced_language = ""

mod = Module()

mod.list("code_extension", "List of file programming languages file extensions")
mod.list("code_language", "List of file programming language identifiers")

mod.tag("code_language_forced", "This tag is active when a language mode is forced")

ctx = Context()

ctx_forced = Context()
ctx_forced.matches = r"""
tag: user.code_language_forced
"""

ctx.lists["self.code_extension"] = {
    **{l.spoken_form: l.extension for l in languages},
    "pie": "py",
}

ctx.lists["self.code_language"] = {l.spoken_form: l.id for l in languages}


@ctx.action_class("code")
class CodeActions:
    def language():
        file_extension = actions.win.file_ext()
        return extension_lang_map.get(file_extension, "")


@ctx_forced.action_class("code")
class ForcedCodeActions:
    def language():
        return forced_language


@mod.action_class
class Actions:
    def code_set_language(language: str):
        """Forces the active programming language to <language> and disables extension matching"""
        global forced_language
        forced_language = language
        # Update tags to force a context refresh. Otherwise `code.language` will not update.
        # Necessary to first set an empty list otherwise you can't move from one forced language to another.
        ctx.tags = []
        ctx.tags = ["user.code_language_forced"]
        actions.user.notify(f"Enabled {language}")

    def code_automatic_language():
        """Clears the forced language and re-enables code.language: extension matching"""
        global forced_language
        forced_language = ""
        ctx.tags = []
        actions.user.notify("Automatic language")
