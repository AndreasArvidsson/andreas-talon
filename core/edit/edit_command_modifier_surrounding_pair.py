from dataclasses import dataclass
from typing import Literal, Optional
from talon import Module, actions
import re

delimiters_map: dict[str, list[str]] = {
    "angleBrackets": ["<", ">"],
    "curlyBrackets": ["{", "}"],
    "parentheses": ["(", ")"],
    "squareBrackets": ["[", "]"],
    "singleQuotes": ["'", "'"],
    "doubleQuotes": ['"', '"'],
    "backtickQuotes": ["`", "`"],
}

mod = Module()


@mod.action_class
class Actions:
    def select_surrounding_pair(delimiter_name: str = "any"):
        """Selects the surrounding pair."""
        pair = get_surrounding_pair_for_selection(delimiter_name)

        actions.edit.left()

        if pair is None:
            return

        for i in range(pair.left_start):
            actions.edit.right()
        for i in range(pair.right_end - pair.left_start):
            actions.edit.extend_right()

    def select_surrounding_pair_interior(delimiter_name: str = "any"):
        """Selects the interior of a surrounding pair."""
        pair = get_surrounding_pair_for_selection(delimiter_name)

        actions.edit.left()

        if pair is None:
            return

        for i in range(pair.left_end):
            actions.edit.right()
        for i in range(pair.right_start - pair.left_end):
            actions.edit.extend_right()


@dataclass
class Document:
    text: str
    selection_start: int
    selection_end: int


@dataclass
class Delimiter:
    delimiter: str
    text: str
    side: Literal["left", "right", "unknown"]


@dataclass
class DelimiterOccurrence:
    delimiter: str
    side: Literal["left", "right", "unknown"]
    start: int
    end: int


@dataclass
class PairOccurrence:
    delimiter: str
    left_start: int
    left_end: int
    right_start: int
    right_end: int


def get_surrounding_pair_for_selection(delimiter_name: str) -> Optional[PairOccurrence]:
    document = get_document_for_selection()
    individual_delimiters = get_individual_delimiters(delimiter_name)
    delimiter_occurrences = get_delimiter_occurrences(
        individual_delimiters, document.text
    )
    pair_occurrences = get_pair_occurrences(
        individual_delimiters, delimiter_occurrences
    )
    start_pair = get_surrounding_pair(pair_occurrences, document.selection_start)

    if document.selection_start == document.selection_end or start_pair is None:
        return start_pair

    end_pair = get_surrounding_pair(pair_occurrences, document.selection_end)

    if end_pair is None:
        return None

    return PairOccurrence(
        start_pair.delimiter,
        start_pair.left_start,
        start_pair.left_end,
        end_pair.right_start,
        end_pair.right_end,
    )


def get_document_for_selection() -> Document:
    selected_text = actions.edit.selected_text()
    if selected_text:
        actions.edit.left()
    actions.edit.extend_line_start()
    pre_text = actions.edit.selected_text()
    actions.edit.select_line()
    line_text = actions.edit.selected_text()
    start_pos = len(pre_text)
    end_pos = start_pos + len(selected_text)
    return Document(line_text, start_pos, end_pos)


def get_surrounding_pair(
    pair_occurrences: list[PairOccurrence],
    position: int,
) -> Optional[PairOccurrence]:
    surrounding_pairs = [
        pair
        for pair in pair_occurrences
        if pair.left_start <= position <= pair.right_end
    ]
    if len(surrounding_pairs) == 0:
        return None
    pair = next(
        (
            pair
            for pair in surrounding_pairs
            if pair.left_start == position or pair.right_start == position
        ),
        None,
    )
    if pair is not None:
        return pair
    surrounding_pairs.sort(key=lambda pair: pair.right_end - pair.left_start)
    return surrounding_pairs[0]


def get_pair_occurrences(
    individual_delimiters: list[Delimiter],
    delimiter_occurrences: list[DelimiterOccurrence],
) -> list[PairOccurrence]:
    open_delimiters: dict[str, list[DelimiterOccurrence]] = {
        delimiter.delimiter: [] for delimiter in individual_delimiters
    }
    result: list[PairOccurrence] = []
    for occurrence in delimiter_occurrences:
        open_list: list[DelimiterOccurrence] = open_delimiters.get(occurrence.delimiter)  # type: ignore
        side = occurrence.side
        if side == "unknown":
            side = "left" if len(open_list) % 2 == 0 else "right"
        if side == "left":
            open_list.append(occurrence)
        elif side == "right":
            open_delimiter = open_list.pop()
            if open_delimiter is not None:
                result.append(
                    PairOccurrence(
                        occurrence.delimiter,
                        open_delimiter.start,
                        open_delimiter.end,
                        occurrence.start,
                        occurrence.end,
                    )
                )
    return result


def get_delimiter_occurrences(
    individual_delimiters: list[Delimiter],
    text: str,
) -> list[DelimiterOccurrence]:
    text_to_delimiter_map = {
        delimiter.text: delimiter for delimiter in individual_delimiters
    }
    delimiter_regex = get_delimiter_regex(individual_delimiters)
    matches = delimiter_regex.finditer(text)
    result: list[DelimiterOccurrence] = []
    for match in matches:
        delimiter = text_to_delimiter_map[match.group()]
        result.append(
            DelimiterOccurrence(delimiter.delimiter, delimiter.side, *match.span())
        )
    return result


def get_delimiter_regex(individual_delimiters: list[Delimiter]) -> re.Pattern[str]:
    unique_delimiter_texts = set(
        [re.escape(delimiter.text) for delimiter in individual_delimiters]
    )
    pattern_string = "|".join(unique_delimiter_texts)
    return re.compile(pattern_string, re.UNICODE)


def get_individual_delimiters(delimiter_name: str):
    delimiter_names = get_delimiter_names(delimiter_name)
    delimiters = []
    for delimiter_name in delimiter_names:
        if delimiter_name not in delimiters_map:
            raise ValueError(f"Unknown delimiter name: {delimiter_name}")
        [left, right] = delimiters_map[delimiter_name]
        is_unique = left != right
        delimiters.append(
            Delimiter(delimiter_name, left, "left" if is_unique else "unknown")
        )
        delimiters.append(
            Delimiter(delimiter_name, right, "right" if is_unique else "unknown")
        )
    return delimiters


def get_delimiter_names(delimiter_name: str) -> list[str]:
    if delimiter_name == "any":
        return [*delimiters_map.keys()]
    elif delimiter_name == "string":
        return ["singleQuotes", "doubleQuotes", "backtickQuotes"]
    return [delimiter_name]
