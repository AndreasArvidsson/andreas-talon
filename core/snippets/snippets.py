from typing import Union
from talon import Module, Context, app, fs, actions
from pathlib import Path
import glob
from ..languages.languages import languages
from .snippets_parser import create_snippets_from_file
from .snippet_types import (
    InsertionSnippet,
    Snippet,
    SnippetLanguageState,
    SnippetLists,
    WrapperSnippet,
)

SNIPPETS_DIR = Path(__file__).parent / "snippets"

mod = Module()

mod.list("snippet", "List of insertion snippets")
mod.list("snippet_with_phrase", "List of insertion snippets containing a text phrase")
mod.list("snippet_wrapper", "List of wrapper snippets")

# {SNIPPET_NAME: Snippet[]}
snippets_map: dict[str, list[Snippet]] = {}

languages_state_map: dict[str, SnippetLanguageState] = {
    # `_` represents the global context, ie snippets available regardless of language
    "_": SnippetLanguageState(Context(), SnippetLists({}, {}, {}))
}

# Create a context for each defined language
for lang in languages:
    ctx = Context()
    ctx.matches = f"code.language: {lang.id}"
    languages_state_map[lang.id] = SnippetLanguageState(ctx, SnippetLists({}, {}, {}))


@mod.action_class
class Actions:
    def get_snippet(name: str) -> Snippet:
        """Get snippet named <name>"""
        return get_snippet_for_active_language(name)

    def get_insertion_snippet(name: str) -> InsertionSnippet:
        """Get insertion snippet named <name>"""
        snippet: Snippet = actions.user.get_snippet(name)
        return InsertionSnippet(snippet.body, snippet.insertion_scopes)

    def get_wrapper_snippet(name: str) -> WrapperSnippet:
        """Get wrapper snippet named <name>"""
        index = name.rindex(".")
        snippet_name = name[:index]
        variable_name = name[index + 1]
        snippet: Snippet = actions.user.get_snippet(snippet_name)
        variable = snippet.get_variable_strict(variable_name)
        return WrapperSnippet(snippet.body, variable.name, variable.wrapper_scope)


def get_snippet_for_active_language(name: str) -> Snippet:
    if name not in snippets_map:
        raise ValueError(f"Unknown snippet '{name}'")

    snippets = snippets_map[name]
    lang: Union[str, set[str]] = actions.code.language()
    languages = list([lang]) if isinstance(lang, str) else lang

    # First try to find a snippet matching the active language
    for snippet in snippets:
        if snippet.languages:
            for snippet_lang in snippet.languages:
                if snippet_lang in languages:
                    return snippet

    for snippet in snippets:
        if not snippet.languages:
            return snippet

    raise ValueError(f"Snippet '{name}' not available for language '{lang}'")


def update_snippets():
    global snippets_map

    snippets = get_snippets_from_files()
    name_to_snippets: dict[str, list[Snippet]] = {}
    language_to_lists: dict[str, SnippetLists] = {}

    for snippet in snippets:
        # Map snippet names to actual snippets
        if snippet.name not in name_to_snippets:
            name_to_snippets[snippet.name] = []
        name_to_snippets[snippet.name].append(snippet)

        # Map languages to phrase / name dicts
        for language in snippet.languages or ["_"]:
            if language not in language_to_lists:
                language_to_lists[language] = SnippetLists({}, {}, {})

            lists = language_to_lists[language]

            for phrase in snippet.phrases or []:
                lists.insertion[phrase] = snippet.name

                for var in snippet.variables:
                    if var.insertion_formatters:
                        lists.with_phrase[phrase] = snippet.name

                    if var.wrapper_phrases:
                        lists.wrapper[phrase] = f"{snippet.name}.{var.name}"

    snippets_map = name_to_snippets
    update_contexts(language_to_lists)


def update_contexts(language_to_lists: dict[str, SnippetLists]):
    for lang, lists in language_to_lists.items():
        if lang not in languages_state_map:
            print(f"Found snippets for unknown language: {lang}")
            continue

        state = languages_state_map[lang]
        updated_lists: dict[str, dict[str, str]] = {}

        if state.lists.insertion != lists.insertion:
            state.lists.insertion = lists.insertion
            updated_lists["user.snippet"] = lists.insertion

        if state.lists.with_phrase != lists.with_phrase:
            state.lists.with_phrase = lists.with_phrase
            updated_lists["user.snippet_with_phrase"] = lists.with_phrase

        if state.lists.wrapper != lists.wrapper:
            state.lists.wrapper = lists.wrapper
            updated_lists["user.snippet_wrapper"] = lists.wrapper

        if updated_lists:
            state.ctx.lists.update(updated_lists)


def get_snippets_from_files() -> list[Snippet]:
    files = glob.glob(f"{SNIPPETS_DIR}/**/*.snippet", recursive=True)
    result = []

    for file in files:
        result.extend(create_snippets_from_file(file))

    return result


def on_ready():
    fs.watch(SNIPPETS_DIR, lambda _1, _2: update_snippets())
    update_snippets()


app.register("ready", on_ready)
