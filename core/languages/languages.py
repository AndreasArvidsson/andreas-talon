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
    Language("talon", "talon", "talon"),
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

mod = Module()

mod.setting(
    "code_language",
    str,
    desc="The identifier of the current active programming language",
)

mod.tag(
    "auto_language",
    desc="If active code language will be automatically detected by file extension",
)
mod.list("code_extension", desc="List of file programming languages file extensions")
mod.list("code_language", desc="List of file programming language identifiers")

ctx_other = Context()

ctx_cmd = Context()
ctx_cmd.matches = r"""
mode: command
"""

ctx_cmd.tags = ["user.auto_language"]

ctx_cmd.lists["self.code_extension"] = {
    **{l.spoken_form: l.extension for l in languages},
    "pie": "py",
    "talon list": "talon-list",
}

ctx_cmd.lists["self.code_language"] = {l.spoken_form: l.id for l in languages}


# Create a context for each defined language
for lang in language_ids:
    mod.tag(lang)
    mod.tag(f"{lang}_forced")
    ctx = Context()
    # Context is active if language is forced or auto language matches
    ctx.matches = f"""
    tag: user.{lang}_forced
    tag: user.auto_language
    and code.language: {lang}
    """
    ctx.tags = [f"user.{lang}"]
    ctx.settings = {"user.code_language": lang}


# Disable `code.language` when not in command mode
@ctx_other.action_class("code")
class CodeActions:
    def language() -> str:
        return ""


@ctx_cmd.action_class("code")
class CodeCommandActions:
    def language() -> str:
        file_extension = actions.win.file_ext()
        if file_extension in extension_lang_map:
            return extension_lang_map[file_extension]
        return ""


@mod.action_class
class Actions:
    def code_set_language(language: str):
        """Sets the active language, and disables extension matching"""
        ctx_cmd.tags = [f"user.{language}_forced"]
        actions.user.notify(f"Enabled {language}")

    def code_automatic_language():
        """Clears the active forced language, and re-enables code.language: extension matching"""
        ctx_cmd.tags = ["user.auto_language"]
        actions.user.notify("Automatic language")
