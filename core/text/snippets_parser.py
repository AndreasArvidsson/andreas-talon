from talon import app
from pathlib import Path
from dataclasses import dataclass
from typing import Union
import glob

SNIPPETS_DIR = Path(__file__).parent / "snippets"


@dataclass
class SnippetVariable:
    name: str
    phrase: str


@dataclass
class Snippet:
    name: str
    body: str
    phrase: str = None
    wrapperScope: str = None
    languages: list[str] = None
    variables: list[SnippetVariable] = None


def parse_snippet_file(path):
    with open(path) as f:
        content = f.read()

    sections = content.split("---")

    default_context = parse_default_context(sections)

    if default_context:
        sections = sections[1:]
    else:
        sections = {}

    snippets = [parse_section(s, default_context) for s in sections]

    for s in snippets:
        print(s)


def parse_default_context(sections: list[str]) -> Union[dict, None]:
    if sections:
        parts = sections[0].split("-")
        if len(parts) == 1:
            return parse_context(parts[0])
    return None


def parse_section(section: str, default_context: dict) -> Snippet:
    parts = section.split("-")

    if len(parts) != 2:
        raise Exception(f"Malformed section: {section}")

    context_str, body = parts

    context = {
        **default_context,
        **parse_context(context_str),
    }

    if not "name" in context:
        raise Exception(f"Missing name: {section}")

    snippet = Snippet(
        name=context["name"],
        body=body.strip(),
    )

    for key, value in context.items():
        match key:
            case "name":
                pass
            case "phrase":
                snippet.phrase = value
            case "wrapperScope":
                snippet.wrapperScope = value
            case "language":
                snippet.languages = [v.strip() for v in value.split(",")]
            case _:
                if not key.startswith("$") and key.endswith(".phrase"):
                    raise Exception(f"Unknown context: '{key}: {value}'")
                variable_name = key[:-7]
                if not variable_name in body:
                    raise Exception(
                        f"Variable '{variable_name}' missing in body '{body}'"
                    )
                if snippet.variables is None:
                    snippet.variables = []
                snippet.variables.append(SnippetVariable(variable_name, value))

    return snippet


def parse_context(context: str) -> dict:
    result = {}
    lines = [l for l in context.splitlines() if l.strip()]

    for line in lines:
        parts = [p.strip() for p in line.split(":")]

        if len(parts) != 2:
            raise Exception(f"Malformed context: {line}")

        key, value = parts
        result[key] = value

    return result


def on_ready():
    files = glob.glob(f"{SNIPPETS_DIR}/*.snippet")

    for file in files:
        parse_snippet_file(file)


app.register("ready", on_ready)
