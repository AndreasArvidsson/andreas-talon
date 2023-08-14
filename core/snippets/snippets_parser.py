from typing import Union
from dataclasses import dataclass
import re
from .snippet_types import Snippet, SnippetVariable


@dataclass
class SnippetDocumentVar:
    name: str
    phrase: str = None
    wrapperScope: str = None


@dataclass
class SnippetDocument:
    variables: list[SnippetDocumentVar]
    name: str = None
    phrase: str = None
    language: list[str] = None
    body: str = None


def parse_snippet_file_from_disk(file_path: str) -> list[Snippet]:
    with open(file_path) as f:
        content = f.read()
    documents = parse_snippet_file(content)
    return create_snippets(documents)


def create_snippets(documents: list[SnippetDocument]) -> list[Snippet]:
    if len(documents) == 0:
        return []

    if documents[0].body is None:
        default_context = documents[0]
        documents = documents[1:]
    else:
        default_context = SnippetDocument([])

    return [create_snippet(d, default_context) for d in documents]


def create_snippet(
    document: SnippetDocument, default_context: SnippetDocument
) -> Snippet:
    name = document.name if document.name else default_context.name
    languages = document.language if document.language else default_context.language
    phrases = document.phrase if document.phrase else default_context.phrase
    body = document.body

    if not name:
        raise ValueError(f"Missing name: {document}")
    if not body:
        raise ValueError(f"Missing body: {document}")

    variables_map = {}

    for variable in [*document.variables, *default_context.variables]:
        if variable.phrase is None:
            raise ValueError(f"Missing variable phrase: {variable}")
        if variable.name in variables_map:
            continue
        var_name = f"${variable.name}"
        if not var_name in body:
            raise Exception(f"Variable '{var_name}' missing in body '{body}'")
        variables_map[variable.name] = SnippetVariable(
            variable.name, variable.phrase, variable.wrapperScope
        )

    variables = list(variables_map.values())

    return Snippet(
        name=name,
        languages=languages,
        phrases=phrases,
        variables=variables,
        body=body,
    )


# ---------- Snippet file parser ----------


def parse_snippet_file(content: str) -> list[SnippetDocument]:
    document_content = re.split(r"^---$", content, flags=re.MULTILINE)
    documents = [parse_document(d) for d in document_content]
    return [d for d in documents if d is not None]


def parse_document(text: str) -> Union[SnippetDocument, None]:
    parts = re.split(r"^-$", text, flags=re.MULTILINE)
    if len(parts) > 2:
        raise ValueError(f"Found multiple '-' in snippet document '{text}'")
    document = parse_context(parts[0])
    if len(parts) == 2:
        body = parse_body(parts[1])
        if body is not None:
            if document is None:
                document = SnippetDocument([])
            document.body = body
    return document


def parse_context(text: str) -> Union[SnippetDocument, None]:
    document = SnippetDocument([])
    pairs = parse_context_pairs(text)

    if len(pairs) == 0:
        return None

    variables: dict[str, str] = {}

    for key, value in pairs.items():
        match key:
            case "name":
                document.name = value
            case "phrase":
                document.phrase = parse_vector_value(value)
            case "language":
                document.language = parse_vector_value(value)
            case _:
                if not key.startswith("$"):
                    raise ValueError(f"Invalid key '${key}'")
                variables[key] = value

    document.variables = parse_variables(variables)

    return document


def parse_context_pairs(text: str) -> dict[str, str]:
    lines = [l.strip() for l in re.split(r"\r?\n", text) if l.strip()]
    pairs: dict[str, str] = {}

    for line in lines:
        parts = line.split(":")
        if len(parts) != 2:
            raise ValueError(f"Invalid line '{line}'")
        key = parts[0].strip()
        value = parts[1].strip()
        if len(key) == 0 or len(value) == 0:
            raise ValueError(f"Invalid line '{line}'")
        if key in pairs:
            raise ValueError(f"Duplicate key '{key}' in '{text}'")
        pairs[key] = value

    return pairs


def parse_variables(variables: dict[str, str]) -> list[SnippetDocumentVar]:
    map: dict[str, SnippetDocumentVar] = {}

    def get_variable(name: str) -> SnippetDocumentVar:
        if name not in map:
            map[name] = SnippetDocumentVar(name)
        return map[name]

    for key, value in variables.items():
        parts = key.split(".")
        if len(parts) != 2:
            raise ValueError(f"Invalid key '{key}'")
        name = parts[0][1:]
        field = parts[1]
        match field:
            case "phrase":
                get_variable(name).phrase = value
            case "wrapperScope":
                get_variable(name).wrapperScope = value
            case _:
                raise ValueError(f"Invalid key '{key}'")

    return list(map.values())


def parse_body(text: str) -> Union[str, None]:
    match_leading = re.search(r"^[ \t]*\S", text, flags=re.MULTILINE)

    if match_leading is None:
        return None

    return text[match_leading.start() :].rstrip()


def parse_vector_value(value: str) -> list[str]:
    return [v.strip() for v in value.split("|")]
