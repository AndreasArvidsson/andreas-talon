from ..core.snippets.snippets_insert_raw_text import parse_snippet
from talon import actions

fixtures = [
    ["stops", "if $1\n\t$0", "if \n    ", 0, 3],
    ["stops {}", "if ${1}\n\t${0}", "if \n    ", 0, 3],
    ["var", "if $condition\n\t$0", "if \n    ", 0, 3],
    ["var {}", "if ${condition}\n\t$0", "if \n    ", 0, 3],
    ["defaults", "if ${condition:True}\n\t${0:return}", "if True\n    return", 0, 3],
    ["order", "if $condition\n\t$1", "if \n    ", 1, 4],
    ["multiple sl", "a $0 $1", "a  ", 0, 3],
]


def test(fixture):
    input = fixture[1]
    expected_body = fixture[2]
    expected_row = fixture[3]
    expected_col = fixture[4]
    body, stop = parse_snippet(input)
    actions.user.assert_equals(expected_body, body)
    actions.user.assert_equals(True, stop is not None, "Stop is None")
    actions.user.assert_equals(expected_row, stop.row, "Row")
    actions.user.assert_equals(expected_col, stop.col, "Col")


def test_snippets_insert_raw():
    actions.user.test_run_suite("snippets insert raw", fixtures, test)
