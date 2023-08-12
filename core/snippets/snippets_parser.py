from typing import Union
import glob
import re
from .snippet_types import Snippet, SnippetVariable

DOC_DELIMITER_RE = re.compile(r"^---$", re.MULTILINE)
BODY_DELIMITER_RE = re.compile(r"^-$", re.MULTILINE)
# Find first line that is not empty. Preserve indentation.
FIRST_CONTENT_LINE_RE = re.compile(r"^[ \t]*\S", re.MULTILINE)


def get_snippets(dir) -> list[Snippet]:
    files = glob.glob(f"{dir}/*.snippet")
    result = []

    for file in files:
        result.extend(parse_snippet_file(file))

    return result


def parse_snippet_file(path) -> list[Snippet]:
    with open(path) as f:
        content = f.read()

    documents = DOC_DELIMITER_RE.split(content)
    default_context = get_default_context(documents)

    if default_context is not None:
        documents = documents[1:]
    else:
        default_context = {}
    return [parse_document(s, default_context) for s in documents]


def get_default_context(sections: list[str]) -> Union[dict[str, str], None]:
    if sections:
        parts = BODY_DELIMITER_RE.split(sections[0])
        if len(parts) == 1:
            return parse_context(parts[0])
    return None


def parse_document(document: str, default_context: dict) -> Snippet:
    parts = BODY_DELIMITER_RE.split(document)

    if len(parts) != 2:
        raise Exception(f"Malformed document: {document}")

    context_str, body = parts

    context = {
        **default_context,
        **parse_context(context_str),
    }

    if not "name" in context:
        raise Exception(f"Missing name: {document}")

    snippet = Snippet(
        name=context["name"],
        body=parse_body(body),
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
                parts = key.split(".")
                var_name, var_field = parts

                if len(parts) != 2 or len(var_name) < 2 or not var_name.startswith("$"):
                    raise Exception(f"Unknown context: '{key}: {value}'")

                if not var_name in body:
                    raise Exception(f"Variable '{var_name}' missing in body '{body}'")

                if snippet.variables is None:
                    snippet.variables = []

                match var_field:
                    case "phrase":
                        snippet.variables.append(
                            SnippetVariable(
                                name=var_name[1:],
                                phrase=value,
                                wrapperScope=context.get(f"{var_name}.wrapperScope"),
                            )
                        )
                    case "wrapperScope":
                        phrase_field = f"{var_name}.phrase"
                        if not phrase_field in context:
                            raise Exception(
                                f"Variable field '{phrase_field}' expected with '{key}'"
                            )
                    case _:
                        raise Exception(
                            f"Unknown variable field '{var_field}' in '{key}'"
                        )

    return snippet


def get_languages(language: str) -> list[str]:
    return [v.strip() for v in language.split("|")]


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


def parse_body(body: str) -> str:
    match_leading = FIRST_CONTENT_LINE_RE.search(body)

    if match_leading is None:
        return ""

    return body[match_leading.start() :].rstrip()
