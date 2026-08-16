import re

from talon import Module, actions

from .snippet_types import Snippet
from .snippets_insert_raw_text import insert_snippet_raw_text

SETTING_RE = re.compile(r"setting\(([\w.]+)\)")

mod = Module()


@mod.action_class
class Actions:
    @staticmethod
    def insert_snippet(body: str):
        """Insert snippet"""
        insert_snippet_raw_text(body)

    @staticmethod
    def insert_snippet_by_name(
        name: str,
        substitutions: dict[str, str] = {},  # noqa: B006
    ):
        """Insert snippet <name>"""
        snippet: Snippet = actions.user.get_snippet(name)
        body = snippet.body

        if substitutions:
            for k, v in substitutions.items():
                placeholders = (f"${k}", f"${{{k}}}")
                found = False
                for placeholder in placeholders:
                    if placeholder in body:
                        body = body.replace(placeholder, v)
                        found = True
                if not found:
                    raise ValueError(
                        f"Can't substitute non existing variable '{k}' in snippet '{name}'"
                    )

        actions.user.insert_snippet(body)

    @staticmethod
    def insert_snippet_by_name_with_phrase(name: str, phrase: str):
        """Insert snippet <name> with phrase <phrase>"""
        snippet: Snippet = actions.user.get_snippet(name)
        substitutions = {}

        for variable in snippet.variables:
            if variable.insertion_formatters is not None:
                formatters = ",".join(variable.insertion_formatters)
                formatters = SETTING_RE.sub(get_setting, formatters)
                formatted_phrase = actions.user.format_text(phrase, formatters)
                substitutions[variable.name] = formatted_phrase

        if not substitutions:
            raise ValueError(
                f"Can't use snippet phrase. No variable with insertion formatter in snippet '{name}'"
            )

        actions.user.insert_snippet_by_name(name, substitutions)


def get_setting(m: re.Match[str]) -> str:
    setting_name = m.group(1)
    try:
        return str(actions.settings.get(setting_name))
    except KeyError as ex:
        raise ValueError(
            f"Undefined formatter setting '{setting_name}' in snippet"
        ) from ex
