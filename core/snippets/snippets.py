from talon import Module, Context, app, fs
from pathlib import Path
from .snippets_parser import get_snippets
from .snippet_types import Snippet

SNIPPETS_DIR = Path(__file__).parent / "snippets"

mod = Module()

mod.list("snippet_insert", desc="List of insertion snippets")
mod.list("snippet_wrap", desc="List of wrapper snippets")

context_map = {}
snippets_map = {}


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

    for lang, snippets in grouped.items():
        if lang != "_" and "_" in grouped:
            snippets = [*grouped["_"], *snippets]

        gm, insertion, wrapper = create_lists(lang, snippets)
        global_map.update(gm)

        if not lang in context_map:
            ctx = Context()
            if lang != "_":
                ctx.matches = f"tag: user.{lang}"
            context_map[lang] = ctx

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
        if snippet.phrase is not None:
            id = f"{prefix}{snippet.name}"
            global_map[id] = snippet
            insertion[snippet.phrase] = id

        if snippet.variables is not None:
            for var in snippet.variables:
                id = f"{prefix}{snippet.name}.{var.name}"
                global_map[id] = snippet
                wrapper[var.phrase] = id

    return global_map, insertion, wrapper


def on_ready():
    fs.watch(str(SNIPPETS_DIR), lambda _1, _2: update_snippets())
    update_snippets()


app.register("ready", on_ready)
