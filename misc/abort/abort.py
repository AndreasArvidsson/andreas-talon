from talon import Module, Context

mod = Module()
setting = mod.setting("abort_phrase", type=str)

mod = Module()
ctx_en = Context()

ctx_sv = Context()
ctx_sv.matches = r"""
language: sv
"""

mod.list("abort_phrase", desc="Phrase used to abort Talon commands")
abort_phrases = ["cancel", "avbryt"]
ctx_en.lists["self.abort_phrase"] = {abort_phrases[0]}
ctx_sv.lists["self.abort_phrase"] = abort_phrases


@mod.action_class
class Actions:
    def abort_phrase(phrase: dict, words: list[str]) -> tuple[bool, str]:
        """Abort current spoken phrase"""
        for abort_phrase in abort_phrases:
            if words[-1] == abort_phrase:
                phrase["parsed"]._sequence = []
                if len(words) > 1:
                    return True, f"... {abort_phrase}"
                return True, abort_phrase
        return False, " ".join(words)
