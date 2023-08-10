from typing import Union
import glob
from .snippet_types import Snippet, SnippetVariable


def get_snippets(dir) -> list[Snippet]:
    files = glob.glob(f"{dir}/*.snippet")
    result = []

    for file in files:
        result.extend(parse_snippet_file(file))

    return result


def parse_snippet_file(path) -> list[Snippet]:
    with open(path) as f:
        content = f.read()

    sections = content.split("---")
    default_context = get_default_context(sections)

    if default_context is not None:
        sections = sections[1:]
    else:
        default_context = {}
    return [parse_section(s, default_context) for s in sections]


def get_default_context(sections: list[str]) -> Union[dict[str, str], None]:
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
                snippet.languages = get_languages(value)
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
                short_name = variable_name[1:]
                snippet.variables.append(SnippetVariable(short_name, value))

    return snippet


def get_languages(language: str) -> list[str]:
    languages_raw = [v.strip() for v in language.split(",")]
    languages = set()
    for lang in languages_raw:
        languages.add(lang)
        match lang:
            case "javascript":
                languages.update({"javascriptreact", "typescript", "typescriptreact"})
            case "javascriptreact":
                languages.add("typescriptreact")
            case "typescript":
                languages.add("typescriptreact")
            case "html":
                languages.update({"javascriptreact", "typescriptreact"})
    result = list(languages)
    result.sort()
    return result


def parse_context(context: str) -> dict[str, str]:
    result = {}
    lines = [l for l in context.splitlines() if l.strip()]

    for line in lines:
        parts = [p.strip() for p in line.split(":")]

        if len(parts) != 2:
            raise Exception(f"Malformed context: {line}")

        key, value = parts
        result[key] = value

    return result
