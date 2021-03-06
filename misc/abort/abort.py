from talon import Module

mod = Module()
setting = mod.setting("abort_word", type=str)


@mod.action_class
class Actions:
    def abort_phrase(phrase: dict, words: list[str]) -> tuple[bool, str]:
        """Abort current spoken phrase"""
        abort_word = setting.get()
        if words[-1] == abort_word:
            phrase["parsed"]._sequence = []
            if len(words) > 1:
                return True, f"... {abort_word}"
            return True, abort_word
        return False, " ".join(words)
