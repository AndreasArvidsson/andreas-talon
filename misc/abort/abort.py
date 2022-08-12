from talon import Module, Context

mod = Module()
setting = mod.setting("abort_word", type=str)

mod = Module()
ctx = Context()

abort_word = "cancel"

mod.list("abort_word", desc="Word used to abort Talon commands")
ctx.lists["self.abort_word"] = {abort_word}


@mod.action_class
class Actions:
    def abort_phrase(phrase: dict, words: list[str]) -> tuple[bool, str]:
        """Abort current spoken phrase"""
        if words[-1] == abort_word:
            phrase["parsed"]._sequence = []
            if len(words) > 1:
                return True, f"... {abort_word}"
            return True, abort_word
        return False, " ".join(words)
