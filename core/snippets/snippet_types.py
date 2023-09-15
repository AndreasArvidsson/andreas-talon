from dataclasses import dataclass


@dataclass
class SnippetVariable:
    name: str
    wrapperPhrases: list[str]
    wrapperScope: str = None


@dataclass
class Snippet:
    name: str
    body: str
    phrases: list[str] = None
    insertionScopes: list[str] = None
    languages: list[str] = None
    variables: list[SnippetVariable] = None
