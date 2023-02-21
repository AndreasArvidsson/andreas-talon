from dataclasses import dataclass
from typing import Optional


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
class WordTiming:
    word: str
    start: float
    end: float

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
    captures: list
    parameters: dict

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
    wordTimings: list[WordTiming]
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
