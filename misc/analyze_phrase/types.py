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
    explanation: Optional[str]

    def get_explanation_or_desc(self):
        return self.explanation or self.ctxDesc or self.modDesc

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
    value: Any
    name: Optional[str]

    def __repr__(self):
        return f"{self.__class__.__name__}({self.__dict__})"


@dataclass
class AnalyzedCommand:
    num: int
    phrase: str
    rule: str
    code: str
    path: str
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