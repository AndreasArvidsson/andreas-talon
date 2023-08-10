from dataclasses import dataclass


@dataclass
class SnippetVariable:
    name: str
    phrase: str
    wrapperScope: str = None


@dataclass
class Snippet:
    name: str
    body: str
    phrase: str = None
    languages: list[str] = None
    variables: list[SnippetVariable] = None
