from talon import Module

abort_word = "cancel"

mod = Module()


@mod.action_class
class Actions:
    def abort_phrase(phrase: dict, words: list[str]) -> tuple[bool, str]:
        """Abort current spoken phrase"""
        if words[-1] == abort_word:
            phrase["parsed"]._sequence = []
            return True, f"... {abort_word}"
        return False, " ".join(words)
