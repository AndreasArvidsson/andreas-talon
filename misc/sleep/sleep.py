from talon import Module, Context, actions
from talon.grammar import Phrase

mod = Module()
ctx_en = Context()

ctx_sv = Context()
ctx_sv.matches = r"""
language: sv
"""

mod.list("sleep_phrase", desc="Phrase used to sleep Talon")
sleep_phrases = ["drowse", "sömnig"]
ctx_en.lists["self.sleep_phrase"] = {sleep_phrases[0]}
ctx_sv.lists["self.sleep_phrase"] = sleep_phrases

time_last_pop = 0


@mod.action_class
class Actions:
    def talon_sleep():
        """Put Talon to sleep"""
        actions.speech.disable()
        actions.user.mouse_sleep()
        actions.user.notify("Talon sleeping")

    def talon_wake():
        """Wake Talon from sleep"""
        actions.user.abort_current_phrase()
        actions.speech.enable()
        actions.user.mouse_wake()
        actions.user.notify("Talon awake")
        if not actions.user.sound_microphone_enabled():
            actions.user.sound_microphone_enable(True)

    def talon_sleep_status():
        """Notify about Talon sleep status"""
        if actions.speech.enabled():
            actions.user.notify("Talon is: awake")
        else:
            actions.user.notify("Talon is: sleeping")

    def talon_sleep_update_phrase(phrase: Phrase) -> tuple[bool, str]:
        """Update spoken phrase in case of sleep command"""
        words = phrase["phrase"]

        for sleep_phrase in sleep_phrases:
            if sleep_phrase in words:
                index = words.index(sleep_phrase)
                text = " ".join(words[: index + 1])
                phrase["phrase"] = words[: index + 1]
                if index < len(words) - 1:
                    text += " ..."
                return True, text

        return False, " ".join(words)
