from talon import Module, actions

mod = Module()

TEXT = "Clipboard content"


@mod.action_class
class Actions:
    def edit_test_paste():
        """Test edit.paste()"""
        actions.clip.set_text(TEXT)
        actions.sleep("100ms")
        test(lambda _: actions.edit.paste())

    def edit_test_paste_text():
        """Test user.paste_text()"""
        test(lambda i: actions.user.paste_text(f"{TEXT} {i}"))


def test(callable):
    actions.key("enter")

    for i in range(100):
        actions.key("[ space")
        callable(i)
        actions.key("space ] enter")
