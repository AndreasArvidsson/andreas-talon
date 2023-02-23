from dataclasses import dataclass
from typing import Optional, Any


@dataclass
class AnalyzedAction:
    code: str
    name: str
    params: str
    desc: str
    explanation: Optional[str]

    def __repr__(self):
        return f"{self.__class__.__name__}({self.__dict__})"


@dataclass
class AnalyzedWord:
    text: str
    start: float
    end: float

    def __repr__(self):
        return f"{self.__class__.__name__}({self.__dict__})"


@dataclass
class AnalyzedCapture:
    phrase: str
    name: str
    value: Any

    def __repr__(self):
        return f"{self.__class__.__name__}({self.__dict__})"


@dataclass
class AnalyzedCommand:
    num: int
    phrase: str
    path: str
    rule: str
    code: str
    line: int
    captures: list[AnalyzedCapture]
    captureMapping: dict

    def __repr__(self):
        return f"{self.__class__.__name__}({self.__dict__})"


@dataclass
class AnalyzedCommandWithActions(AnalyzedCommand):
    actions: list[AnalyzedAction]

    def __repr__(self):
        return f"{self.__class__.__name__}({self.__dict__})"


@dataclass
class AnalyzedPhraseBase:
    phrase: str
    words: list[AnalyzedWord]
    rawSim: str

    def __repr__(self):
        return f"{self.__class__.__name__}({self.__dict__})"


@dataclass
class AnalyzedPhrase(AnalyzedPhraseBase):
    commands: list[AnalyzedCommand]

    def __repr__(self):
        return f"{self.__class__.__name__}({self.__dict__})"


@dataclass
class AnalyzedPhraseWithActions(AnalyzedPhraseBase):
    commands: list[AnalyzedCommandWithActions]

    def __repr__(self):
        return f"{self.__class__.__name__}({self.__dict__})"
