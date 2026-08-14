import talon

if hasattr(talon, "test_mode"):
    import pytest

    from core.snippets.snippets_insert_raw_text import parse_snippet

    fixtures = [
        ["stops", "if $1\n\t$0", "if \n    ", 0, 3],
        ["stops {}", "if ${1}\n\t${0}", "if \n    ", 0, 3],
        ["var", "if $condition\n\t$0", "if \n    ", 0, 3],
        ["var {}", "if ${condition}\n\t$0", "if \n    ", 0, 3],
        [
            "defaults",
            "if ${condition:True}\n\t${0:return}",
            "if True\n    return",
            0,
            3,
        ],
        ["order", "if $condition\n\t$1", "if \n    ", 1, 4],
        ["multiple sl", "a $0 $1", "a  ", 0, 3],
    ]

    @pytest.mark.parametrize(
        "fixture",
        [pytest.param(fixture, id=fixture[0]) for fixture in fixtures],
    )
    def test_snippets_insert_raw(fixture):
        _, input_text, expected_body, expected_row, expected_col = fixture
        body, stop = parse_snippet(input_text)

        assert body == expected_body
        assert stop is not None
        assert stop.row == expected_row
        assert stop.col == expected_col
