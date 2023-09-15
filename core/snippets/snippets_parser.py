from typing import Union
from dataclasses import dataclass
import re
from .snippet_types import Snippet, SnippetVariable


@dataclass
class SnippetDocumentVar:
    name: str
    wrapperPhrases: list[str] = None
    wrapperScope: str = None


@dataclass
class SnippetDocument:
    variables: list[SnippetDocumentVar]
    name: str = None
    phrases: list[str] = None
    insertionScopes: list[str] = None
    languages: list[str] = None
    body: str = None


def parse_snippet_file_from_disk(file_path: str) -> list[Snippet]:
    with open(file_path, encoding="utf-8") as f:
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
    languages = document.languages if document.languages else default_context.languages
    phrases = document.phrases if document.phrases else default_context.phrases
    body = normalize_snippet_body_tabs(document.body)

    if not name:
        raise ValueError(f"Missing name: {document}")
    if not body:
        raise ValueError(f"Missing body: {document}")

    variables: dict[str, SnippetVariable] = {}

    for variable in [*default_context.variables, *document.variables]:
        if variable.wrapperPhrases is None:
            raise ValueError(f"Missing variable phrase: {variable}")
        if variable.name in variables:
            continue
        var_name = f"${variable.name}"
        if not var_name in body:
            raise ValueError(f"Variable '{var_name}' missing in body '{body}'")
        variables[variable.name] = SnippetVariable(
            variable.name, variable.wrapperPhrases, variable.wrapperScope
        )

    return Snippet(
        name=name,
        languages=languages,
        phrases=phrases,
        variables=list(variables.values()),
        body=body,
    )


def normalize_snippet_body_tabs(body: str) -> str:
    # If snippet body already contains tabs. No change.
    if "\t" in body:
        return body

    lines = []
    smallest_indentation = None

    for line in re.split(r"\r?\n", body):
        match = re.search(r"^\s+", line)
        indentation = match.group() if match is not None else ""

        # Keep track of smallest non-empty indentation
        if len(indentation) > 0 and (
            smallest_indentation is None or len(indentation) < len(smallest_indentation)
        ):
            smallest_indentation = indentation

        lines.append({"indentation": indentation, "rest": line[len(indentation) :]})

    # No indentation found in snippet body. No change.
    if smallest_indentation is None:
        return body

    normalized_lines = [
        reconstruct_line(smallest_indentation, line["indentation"], line["rest"])
        for line in lines
    ]

    return "\n".join(normalized_lines)


def reconstruct_line(smallest_indentation: str, indentation: str, rest: str) -> str:
    # Update indentation by replacing each occurrent of smallest space indentation with a tab
    indentation = indentation.replace(smallest_indentation, "\t")
    return f"{indentation}{rest}"


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
                document.phrases = parse_vector_value(value)
            case "insertionScope":
                document.insertionScopes = parse_vector_value(value)
            case "language":
                document.languages = parse_vector_value(value)
            case _:
                if not key.startswith("$"):
                    raise ValueError(f"Invalid key '{key}'")
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
    variables_map: dict[str, SnippetDocumentVar] = {}

    def get_variable(name: str) -> SnippetDocumentVar:
        if name not in variables_map:
            variables_map[name] = SnippetDocumentVar(name)
        return variables_map[name]

    for key, value in variables.items():
        parts = key.split(".")
        if len(parts) != 2:
            raise ValueError(f"Invalid variable key '{key}'")
        name = parts[0][1:]
        field = parts[1]
        match field:
            case "wrapperPhrase":
                get_variable(name).wrapperPhrases = parse_vector_value(value)
            case "wrapperScope":
                get_variable(name).wrapperScope = value
            case _:
                raise ValueError(f"Invalid variable key '{key}'")

    return list(variables_map.values())


def parse_body(text: str) -> Union[str, None]:
    match_leading = re.search(r"^[ \t]*\S", text, flags=re.MULTILINE)

    if match_leading is None:
        return None

    return text[match_leading.start() :].rstrip()


def parse_vector_value(value: str) -> list[str]:
    return [v.strip() for v in value.split("|")]
