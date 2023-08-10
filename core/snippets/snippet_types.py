from dataclasses import dataclass


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
