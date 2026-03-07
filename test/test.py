from typing import Any, Callable

from talon import Module, actions, app  # pyright: ignore[reportUnusedImport] # noqa: F401

from .command_description_test import test_get_action_explanation
from .formatters_test import test_formatters
from .snippets_insert_raw_test import test_snippets_insert_raw


def run_tests():
    print("")
    test_formatters()
    test_get_action_explanation()
    test_snippets_insert_raw()


# app.register("ready", run_tests)


mod = Module()


@mod.action_class
class Actions:
    @staticmethod
    def test_run_suite(suite_name: str, fixtures: list, callback: Callable):
        """Start a new test suite"""
        print(f"---- START | {suite_name} | {len(fixtures)}")
        succeeded = 0
        failed = 0
        for fixture in fixtures:
            test_name = fixture[0]
            try:
                callback(fixture)
                succeeded += 1
                # print(f" OK  | {test_name}")
            except AssertionError as ex:
                failed += 1
                print(f"FAIL | {test_name}")
                print(ex)
                print("")
        print(f"---- END | {suite_name} | succeeded: {succeeded} | failed: {failed}\n")
        if failed:
            actions.app.notify(f"{failed} tests failed")

    @staticmethod
    def assert_equals(expected: Any, found: Any, message: str = ""):
        """Assert that the values are equal"""
        msg = f"Expected: '{expected}' | Found: '{found}'"
        if message:
            msg = f"{message} | {msg}"
        assert expected == found, msg
