from talon import Context, Module, actions
from dataclasses import dataclass

mod = Module()
ctx = Context()

extension_lang_map = {
    ".asm": "assembly",
    ".bashbook": "bash",
    ".bat": "batch",
    ".c": "c",
    ".cmake": "cmake",
    ".cpp": "cplusplus",
    ".cs": "csharp",
    ".csv": "csv",
    ".gdb": "gdb",
    ".go": "go",
    ".h": "c",
    ".hpp": "cplusplus",
    ".html": "html",
    ".java": "java",
    ".js": "javascript",
    ".json": "json",
    ".jsx": "javascriptreact",
    ".lua": "lua",
    ".md": "markdown",
    ".pl": "perl",
    ".ps1": "powershell",
    ".py": "python",
    ".r": "r",
    ".rb": "ruby",
    ".s": "assembly",
    ".sh": "bash",
    ".snippets": "snippets",
    ".talon": "talon",
    ".ts": "typescript",
    ".tsx": "typescriptreact",
    ".vba": "vba",
    ".vim": "vimscript",
    ".vimrc": "vimscript",
}


@dataclass
class Language:
    id: str
    file_ending: str
    spoken_form: str
    # file_ending_spoken_form: str?


languages = [
    Language("plaintext", "txt", "text"),
    Language("talon", "talon", "talon"),
    Language("python", "py", "pie"),  # pie and python?
    Language("markdown", "md", "mark down"),
    Language("lua", "lua", "lua"),
    Language("c", "c", "see"),
    Language("html", "html", "html"),
    Language("json", "json", "json"),
    Language("java", "java", "java"),
    Language("xml", "xml", "xml"),
    Language("csv", "csv", "csv"),
    Language("exe", "exe", "exe"),
    Language("shellscript", "sh", "shell script"),
    Language("cplusplus", "cpp", "see plus plus"),
    Language("csharp", "cs", "see sharp"),
    Language("typescript", "ts", "type script"),
    Language("typescriptreact", "tsx", "type script react"),
    Language("javascript", "js", "java script"),
    Language("javascriptreact", "jsx", "java script react"),
]

# mod.list("key_modifier", desc="All modifier keys")
# ctx.lists["self.key_modifier"] = { }
# update extensions.py

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


@mod.action_class
class Actions:
    def code_set_language_mode(language: str):
        """Sets the active language mode, and disables extension matching"""
        ctx.tags = [f"user.{language}_forced"]
        actions.user.notify(f"Enabled {language} mode")

    def code_clear_language_mode():
        """Clears the active language mode, and re-enables code.language: extension matching"""
        ctx.tags = ["user.auto_lang"]
