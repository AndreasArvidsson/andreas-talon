from talon import Context, Module, actions
from typing import Union
from dataclasses import dataclass


@dataclass
class Language:
    id: str
    spoken_form: str
    extensions: list[str]


code_languages = [
    Language("bash", "bash", ["sh", "bashbook"]),
    Language("batch", "batch", ["bat"]),
    Language("c", "see", ["c", "h"]),
    Language("cpp", "see plus plus", ["cpp"]),
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
    Language("python", "python", ["py", "ipynb"]),
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
    Language("yaml", "yaml", ["yaml"]),
]

mod = Module()
ctx = Context()

ctx_forced = Context()
ctx_forced.matches = r"""
tag: user.code_language_forced
"""

mod.tag("code_language_forced", "This tag is active when a language mode is forced")
mod.list("code_extension", "List of file programming languages file extensions")
mod.list("code_language", "List of file programming language identifiers")

ctx.lists["user.code_language"] = {lang.spoken_form: lang.id for lang in code_languages}

ctx.lists["user.code_extension"] = {
    **{lang.spoken_form: lang.extensions[0] for lang in code_languages},
    "pie": "py",
}

# Maps extension to language ids
extension_lang_map = {
    f".{ext}": lang.id for lang in code_languages for ext in lang.extensions
}

forced_language = ""


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
