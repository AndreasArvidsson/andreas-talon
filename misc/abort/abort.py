from talon import Module, Context, actions
import time

mod = Module()

ctx_en = Context()

ctx_sv = Context()
ctx_sv.matches = r"""
language: sv
"""

mod.list("abort_phrase", desc="Phrase used to abort Talon commands")
abort_phrases = ["cancel", "canceled", "avbryt"]
ctx_en.lists["self.abort_phrase"] = abort_phrases[:2]
ctx_sv.lists["self.abort_phrase"] = abort_phrases

ts_threshold = None


@mod.action_class
class Actions:
    def abort_current_phrase():
        """Abort current phrase"""
        global ts_threshold
        ts_threshold = time.perf_counter()

    def abort_phrase(phrase: dict, words: list[str]) -> tuple[bool, str]:
        """Abort current spoken phrase"""
        global ts_threshold

        if ts_threshold is not None:
            delta = ts_threshold - phrase["_ts"]
            ts_threshold = None
            if delta > 0:
                actions.user.debug(f"Aborted phrase. {delta:.2f}s")
                phrase["parsed"]._sequence = []
                return True, ""

        for abort_phrase in abort_phrases:
            if words[-1] == abort_phrase:
                phrase["parsed"]._sequence = []
                if len(words) > 1:
                    return True, f"... {abort_phrase}"
                return True, abort_phrase

        return False, " ".join(words)
