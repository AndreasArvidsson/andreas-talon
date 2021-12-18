from talon import Module, actions, app
from typing import Any
from .formatters_test import test_formatters


def run_tests():
    print("")
    test_formatters()


# app.register("ready", run_tests)


mod = Module()


@mod.action_class
class Actions:
    def test_run_suite(suite_name: str, fixtures: list, callback: callable):
        """Start a new test suite"""
        print(f"---- START | {suite_name} | {len(fixtures)}")
        succeeded = 0
        failed = 0
        for fixture in fixtures:
            test_name = fixture[0]
            try:
                callback(fixture)
                succeeded += 1
                print(f" OK  | {test_name}")
            except AssertionError as ex:
                failed += 1
                print(f"FAIL | {test_name}")
                print(ex)
        print(f"---- END | {suite_name} | succeeded: {succeeded} | failed: {failed}\n")
        if failed:
            actions.app.notify(f"{failed} tests failed")

    def assert_equals(expected: Any, found: Any, message: str = ""):
        """Assert that the values are equal"""
        msg = f"Expected: '{expected}' | Found: '{found}'"
        if message:
            msg = f"{message} | {msg}"
        assert expected == found, msg
