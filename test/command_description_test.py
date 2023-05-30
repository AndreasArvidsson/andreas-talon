from ..core.on_phrase.analyze_phrase.calc_command_actions import get_action_explanation
from talon import actions


def test_get_action_explanation():
    def get_print(name: str, params: str, expected: str = None):
        return [
            name,
            "print",
            params,
            ["obj"],
            "Module description",
            None,
            {"prose": "hello world"},
            f"Log text '{expected or 'hello world'}'",
        ]

    def get_key(name: str, params: str, expected: str):
        return [
            name,
            "key",
            params,
            ["key"],
            "Module description",
            None,
            {"letter": "a b"},
            expected,
        ]

    def get_vscode(name: str, expected: str = ""):
        return [
            name,
            f"user.{name}",
            "edit.command",
            ["command_id"],
            "Execute vscode command <command_id>" + expected,
            None,
            {},
            f"Execute vscode command 'edit.command'" + expected,
        ]

    def get_desc(name: str, mod: str, ctx: str, expected: str):
        return [name, "my_action", "hello world", ["text"], mod, ctx, {}, expected]

    fixtures = [
        get_print("print1", "hello world"),
        get_print("print2", "prose"),
        get_print("print3", "'{prose}'"),
        get_print("print4", '"{prose}"'),
        get_print("print5", '"say {prose}!"', "say hello world!"),
        [
            "print6",
            "print",
            "\"a {number_small} b {number_small_2 or 'X'} c {number_small}\"",
            ["obj"],
            "Module description",
            None,
            {"number_small": 1},
            "Log text 'a 1 b X c 1'",
        ],
        [
            "print7",
            "print",
            "\"a {number_small} b {number_small_2 or 'X'} c {number_small}\"",
            ["obj"],
            "Module description",
            None,
            {"number_small": 1, "number_small_2": 2},
            "Log text 'a 1 b 2 c 1'",
        ],
        get_key("key1", "a", "Press key 'a'"),
        get_key("key2", "a b", "Press keys 'a b'"),
        get_key("key3", "ctrl-a", "Press keys 'ctrl-a'"),
        get_key("key4", "letter", "Press keys 'a b'"),
        get_key("key5", "'{letter}'", "Press keys 'a b'"),
        get_key("key6", '"{letter}"', "Press keys 'a b'"),
        get_key("key7", '"{letter} c"', "Press keys 'a b c'"),
        get_vscode("vscode"),
        get_vscode("vscode_get", " with return value"),
        get_desc(
            "mod desc",
            "Module description <text>",
            None,
            "Module description 'hello world'",
        ),
        get_desc(
            "ctx desc",
            "Module description <text>",
            "Context description <text>",
            "Context description 'hello world'",
        ),
        [
            "formatter",
            "my_action",
            'prose, "ALL_CAPS"',
            ["text", "formatters"],
            "Module description",
            "Insert text <text> formatted as <formatters>",
            {"prose": "hello world"},
            "Insert text 'hello world' formatted as 'ALL_CAPS'",
        ],
    ]

    def test(fixture):
        params = fixture[1:-1]
        expected = fixture[-1]
        found = get_action_explanation(*params)
        actions.user.assert_equals(expected, found)

    actions.user.test_run_suite("get_action_explanation", fixtures, test)
