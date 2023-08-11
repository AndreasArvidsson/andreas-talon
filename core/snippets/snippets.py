from talon import Module, Context, app, fs
from pathlib import Path
from ..languages.languages import language_ids
from .snippets_parser import get_snippets
from .snippet_types import Snippet

SNIPPETS_DIR = Path(__file__).parent / "snippets"

mod = Module()

mod.list("snippet_insert", desc="List of insertion snippets")
mod.list("snippet_wrap", desc="List of wrapper snippets")

context_map = {
    "_": Context(),
}
snippets_map = {}

# Create a context for each defined language
for lang in language_ids:
    ctx = Context()
    ctx.matches = f"tag: user.{lang}"
    context_map[lang] = ctx


@mod.action_class
class Actions:
    def get_snippet(id: str) -> Snippet:
        """Get snippet by <id>"""
        return snippets_map[id]


def update_snippets():
    global snippets_map
    grouped = group_by_language(
        get_snippets(SNIPPETS_DIR),
    )

    global_map = {}
    _, global_insertion, global_wrapper = create_lists("_", grouped.get("_", []))

    for lang, snippets in grouped.items():
        gm, insertion, wrapper = create_lists(lang, snippets)
        global_map.update(gm)

        if lang != "_":
            insertion = {**global_insertion, **insertion}
            wrapper = {**global_wrapper, **wrapper}

        ctx = context_map[lang]
        ctx.lists["user.snippet_insert"] = insertion
        ctx.lists["user.snippet_wrap"] = wrapper

    snippets_map = global_map


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
    global_map = {}
    insertion = {}
    wrapper = {}
    prefix = "" if lang == "_" else f"{lang}."

    for snippet in snippets:
        snippet_id = f"{prefix}{snippet.name}"
        global_map[snippet_id] = snippet

        if snippet.phrase is not None:
            insertion[snippet.phrase] = snippet_id

        if snippet.variables is not None:
            for var in snippet.variables:
                wrapper[var.phrase] = f"{snippet_id}.{var.name}"

    return global_map, insertion, wrapper


def on_ready():
    fs.watch(str(SNIPPETS_DIR), lambda _1, _2: update_snippets())
    update_snippets()


app.register("ready", on_ready)
