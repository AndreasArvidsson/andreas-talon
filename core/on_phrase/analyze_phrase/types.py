from dataclasses import dataclass
from typing import Optional, Any


@dataclass
class AnalyzedAction:
    code: str
    name: str
    params: Optional[str]
    path: str
    line: Optional[float]
    modDesc: str
    ctxDesc: Optional[str]
    explanation: str

    def __repr__(self):
        return f"{self.__class__.__name__}({self.__dict__})"


@dataclass
class AnalyzedWord:
    text: str
    start: Optional[float]
    end: Optional[float]

    def __repr__(self):
        return f"{self.__class__.__name__}({self.__dict__})"


@dataclass
class AnalyzedCapture:
    phrase: str
    value: Any
    name: Optional[str]

    def __repr__(self):
        return f"{self.__class__.__name__}({self.__dict__})"


@dataclass
class AnalyzedCommand:
    phrase: str
    rule: str
    code: str
    path: str
    line: int
    captures: list[AnalyzedCapture]
    captureMapping: dict
    actions: list[AnalyzedAction]

    def __repr__(self):
        return f"{self.__class__.__name__}({self.__dict__})"


@dataclass
class AnalyzedPhrase:
    phrase: str
    words: list[AnalyzedWord]
    metadata: Optional[dict]
    commands: list[AnalyzedCommand]

    def __repr__(self):
        return f"{self.__class__.__name__}({self.__dict__})"
