from talon import Context, Module, actions
from typing import Union
from dataclasses import dataclass


@dataclass
class Language:
    id: str
    spoken_form: str
    extensions: list[str]


languages = [
    Language("batch", "batch", ["bat"]),
    Language("c", "see", ["c"]),
    Language("cpp", "see plus plus", ["cpp", "h"]),
    Language("csharp", "see sharp", ["cs"]),
    Language("css", "css", ["css"]),
    Language("csv", "csv", ["csv"]),
    Language("go", "go", ["go"]),
    Language("html", "html", ["html"]),
    Language("java", "java", ["java"]),
    Language("javascript", "java script", ["js", "mjs", "cjs"]),
    Language("javascriptreact", "java script react", ["jsx"]),
    Language("json", "json", ["json"]),
    Language("jsonl", "json lines", ["jsonl"]),
    Language("lua", "lua", ["lua"]),
    Language("markdown", "mark down", ["md"]),
    Language("perl", "perl", ["pl"]),
    Language("plaintext", "text", ["txt"]),
    Language("powershell", "power shell", ["ps1"]),
    Language("python", "python", ["py"]),
    Language("r", "are", ["r"]),
    Language("ruby", "ruby", ["rb"]),
    Language("scm", "tree sitter", ["scm"]),
    Language("scss", "scss", ["scss"]),
    Language("shellscript", "shell script", ["sh"]),
    Language("snippet", "snippet", ["snippet"]),
    Language("talon-list", "talon list", ["talon-list"]),
    Language("talon", "talon", ["talon"]),
    Language("typescript", "type script", ["ts", "mts", "cts"]),
    Language("typescriptreact", "type script react", ["tsx"]),
    Language("xml", "xml", ["xml"]),
]

extension_lang_map = {
    **{f".{ext}": lang.id for lang in languages for ext in lang.extensions},
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

ctx.lists["user.code_extension"] = {
    **{lang.spoken_form: lang.extensions[0] for lang in languages},
    "pie": "py",
}

ctx.lists["user.code_language"] = {lang.spoken_form: lang.id for lang in languages}


@ctx.action_class("code")
class CodeActions:
    def language() -> Union[str, set[str]]:
        file_extension = actions.win.file_ext()
        return extension_lang_map.get(file_extension, "")


@ctx_forced.action_class("code")
class ForcedCodeActions:
    def language() -> Union[str, set[str]]:
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
