import time
from talon import Module, actions

mod = Module()

TEXT = "Clipboard_content"


@mod.action_class
class Actions:
    def edit_test_paste():
        """Test edit.paste()"""
        actions.clip.set_text(TEXT)
        actions.sleep("100ms")
        test(lambda _: actions.edit.paste())

    def edit_test_paste_text():
        """Test user.paste_text()"""
        test(lambda i: actions.user.paste_text(f"{TEXT}_{i}"))

    def edit_test_insert():
        """Test insert()"""
        test(lambda i: actions.insert(f"{TEXT}_{i}"))

    def edit_test_paste_text_performance():
        """Test user.paste_text() performance"""
        test_performance(
            "insert",
            "user.paste_text",
            actions.insert,
            actions.user.paste_text,
        )


def test(callable):
    t1 = time.perf_counter()
    actions.key("enter")

    for i in range(100):
        actions.key("[ space")
        callable(i)
        actions.key("space ] enter")

    t2 = time.perf_counter()
    actions.insert(f"\nTest completed in {int((t2-t1)*1000)}ms")


def test_performance(name1, name2, callable1, callable2):
    text = ""

    for i in range(60):
        text += "-"
        test_single_callback_performance(name1, callable1, i, text)
        test_single_callback_performance(name2, callable2, i, text)


def test_single_callback_performance(name, callable, index, text):
    t1 = time.perf_counter()
    callable(f"{text}")
    t2 = time.perf_counter()
    actions.insert(f"\n{index} {name}: {int((t2-t1)*1000)}ms\n\n")
