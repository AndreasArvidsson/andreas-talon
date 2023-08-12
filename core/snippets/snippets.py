from talon import Module, Context, app, fs
from pathlib import Path
from ..languages.languages import language_ids
from .snippets_parser import get_snippets
from .snippet_types import Snippet

SNIPPETS_DIR = Path(__file__).parent / "snippets"

mod = Module()

mod.list("snippet_insert", "List of insertion snippets")
mod.list("snippet_wrap", "List of wrapper snippets")

context_map = {
    "_": Context(),
}
snippets_map = {}

# Create a context for each defined language
for lang in language_ids:
    ctx = Context()
    ctx.matches = f"code.language: {lang}"
    context_map[lang] = ctx


@mod.action_class
class Actions:
    def get_snippet(id: str) -> Snippet:
        """Get snippet by <id>"""
        return snippets_map[id]


def update_snippets():
    grouped = group_by_language(get_snippets(SNIPPETS_DIR))

    snippets_map.clear()

    for lang, ctx in context_map.items():
        insertion_map = {}
        wrapper_map = {}

        for fl in get_fallback_languages(lang):
            _, insertions, wrappers = create_lists(fl, grouped.get(fl, []))
            insertion_map.update(insertions)
            wrapper_map.update(wrappers)

        snippets, insertions, wrappers = create_lists(lang, grouped.get(lang, []))
        snippets_map.update(snippets)
        insertion_map.update(insertions)
        wrapper_map.update(wrappers)

        ctx.lists["user.snippet_insert"] = insertion_map
        ctx.lists["user.snippet_wrap"] = wrapper_map


def get_fallback_languages(language: str) -> list[str]:
    match language:
        case "_":
            return []
        case "typescript":
            return ["_", "javascript"]
        case "javascriptreact":
            return ["_", "html", "javascript"]
        case "typescriptreact":
            return ["_", "html", "javascript", "typescript", "javascriptreact"]
        case _:
            return ["_"]


def group_by_language(snippets: list[Snippet]) -> dict[str, list[Snippet]]:
    result = {}
    for snippet in snippets:
        if snippet.languages is not None:
            for lang in snippet.languages:
                if not lang in result:
                    result[lang] = []
                result[lang].append(snippet)
        else:
            if not "_" in result:
                result["_"] = []
            result["_"].append(snippet)
    return result


def create_lists(
    lang: str, snippets: list[Snippet]
) -> tuple[dict[str, list[Snippet]], dict[str, str], dict[str, str]]:
    snippets_map = {}
    insertions = {}
    wrappers = {}
    prefix = "" if lang == "_" else f"{lang}."

    for snippet in snippets:
        snippet_id = f"{prefix}{snippet.name}"
        snippets_map[snippet_id] = snippet

        if snippet.phrase is not None:
            insertions[snippet.phrase] = snippet_id

        if snippet.variables is not None:
            for var in snippet.variables:
                wrappers[var.phrase] = f"{snippet_id}.{var.name}"

    return snippets_map, insertions, wrappers


def on_ready():
    fs.watch(str(SNIPPETS_DIR), lambda _1, _2: update_snippets())
    update_snippets()


app.register("ready", on_ready)
