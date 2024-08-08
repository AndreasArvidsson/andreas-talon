from typing import Optional
from talon import Context, ui
from talon.windows.ax import TextRange


ctx = Context()


@ctx.action_class("user")
class Actions:
    def dictation_get_context() -> tuple[Optional[str], Optional[str]]:
        try:
            return dictation_get_context()
        except Exception as e:
            print(e)
            return (None, None)


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

    text_before = get_text_from_range(selection_range_before, -1)
    text_after = get_text_from_range(selection_range_after, 0)
    # print(f"'{text_before}'", f"'{text_after}'")

    return (text_before, text_after)


def move_endpoint_with_boundary(
    target_range: TextRange,
    boundary_range: TextRange,
    endpoint,
    iterations: int,
    delta: int,
):
    for _ in range(iterations):
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
    return text.splitlines()[index]
