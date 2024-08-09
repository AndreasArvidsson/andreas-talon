from typing import Optional
from talon import Context, ui
from talon.windows.ax import TextRange


ctx = Context()


# @ctx.action_class("user")
# class Actions:
#     def dictation_get_context() -> tuple[Optional[str], Optional[str]]:
#         try:
#             return dictation_get_context()
#         except Exception as e:
#             print(e)
#             return (None, None)


def dictation_get_context() -> tuple[Optional[str], Optional[str]]:
    el = ui.focused_element()
    text_pattern = el.text_pattern2
    document_range = text_pattern.document_range
    selection_ranges = text_pattern.selection

    if len(selection_ranges) != 1:
        raise ValueError("Expected singe selection range")

    selection_range_before = selection_ranges[0].clone()
    selection_range_after = selection_ranges[0].clone()

    move_endpoint_with_boundary(selection_range_before, document_range, "Start", 2, -1)
    move_endpoint_with_boundary(selection_range_after, document_range, "End", 2, 1)

    print(get_selection(document_range, selection_ranges[0], text_pattern.caret_range))

    # print(f"'{document_range.text}'")
    print(document_range.text.splitlines())

    b = selection_range_before.text.replace("\n", "\\n")
    a = selection_range_after.text.replace("\n", "\\n")
    print(f"'{b}'", f"'{a}'")

    text_before = get_text_from_range(selection_range_before, -1)
    text_after = get_text_from_range(selection_range_after, 0)

    # print(f"'{text_before}'", f"'{text_after}'")

    return (text_before, text_after)


def move_endpoint_with_boundary(
    target_range: TextRange,
    boundary_range: TextRange,
    endpoint,
    count: int,
    delta: int,
):
    for _ in range(count):
        # If we reach the boundary endpoint we stop
        if (
            target_range.compare_endpoints(endpoint, endpoint, target=boundary_range)
            == 0
        ):
            break
        target_range.move_endpoint_by_unit(endpoint, "Character", delta)


def get_text_from_range(text_range: TextRange, index: int) -> str:
    text = text_range.text
    if text == "":
        return ""
    # We don't want to include or step over new lines.
    # print(text.splitlines())
    return text.splitlines()[index]


def get_selection(
    document_range: TextRange, selection_range: TextRange, caret_range: TextRange
) -> tuple[int, int]:
    # Make copy of the document range to avoid modifying the original
    range_before_selection = document_range.clone()
    # Move the end of the copy to the start of the selection
    # range_before_selection.end = selection_range.start
    range_before_selection.move_endpoint_by_range(
        "End",
        "Start",
        target=selection_range,
    )
    # The selection start offset is the length of the text before the selection
    start = len(range_before_selection.text)
    print(f"'{range_before_selection.text}'")

    range_after_selection = document_range.clone()
    range_after_selection.move_endpoint_by_range(
        "Start",
        "End",
        target=selection_range,
    )
    end = len(document_range.text) - len(range_after_selection.text)

    # The selection is reversed if the caret is at the start of the selection
    is_reversed = (
        caret_range.compare_endpoints("Start", "Start", target=selection_range) == 0
    )

    # Return as (anchor, active)
    return (end, start) if is_reversed else (start, end)
