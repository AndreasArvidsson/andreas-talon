from typing import Optional
from talon import Module, Context, actions
from talon.grammar import Phrase, Capture
from talon.grammar.vm import VMCapture
from talon.engines.w2l import DecodeWord
from dataclasses import dataclass
import time

mod = Module()
ctx = Context()

ctx_sv = Context()
ctx_sv.matches = r"""
language: sv
"""

mod.list("abort_phrase", "Phrase used to abort/cancel current spoken phrase")

abort_phrases = {
    "cancel": "cancel",
    "avbryt": "avbryt",
    # Substitutes for cancel
    "canceled": "cancel",
    "castle": "cancel",
}

ctx.lists["user.abort_phrase"] = {"cancel"}
ctx_sv.lists["user.abort_phrase"] = {"cancel", "avbryt"}


@dataclass
class AbortPhrases:
    phrases: list[str]
    start: float
    end: float


abort_specific_phrases: Optional[AbortPhrases] = None
ts_threshold: float = 0


@mod.action_class
class Actions:
    def abort_current_phrase():
        """Abort current spoken phrase"""
        global ts_threshold
        ts_threshold = time.perf_counter()

    def abort_specific_phrases(phrases: list[str], start: float, end: float):
        """Abort the specified phrases"""
        global abort_specific_phrases
        abort_specific_phrases = AbortPhrases(phrases, start, end)

    # This action only exists so the command history can have a docstring.
    def abort_phrase_command():
        """Abort/cancel current spoken phrase"""
        actions.skip()


def abort_update_phrase(phrase: Phrase) -> tuple[bool, str]:
    """Possibly abort current spoken phrase"""
    global ts_threshold, abort_specific_phrases

    words = phrase["phrase"]
    current_phrase = " ".join(words)

    if abort_specific_phrases is not None:
        if current_phrase in abort_specific_phrases.phrases:
            # Abort phrase if timestamps overlap with aborted phrases
            start = getattr(words[0], "start", 0)
            end = getattr(words[-1], "end", 0)
            if intersects(
                abort_specific_phrases.start, abort_specific_phrases.end, start, end
            ):
                actions.user.debug(f"Aborted phrase: {current_phrase}")
                abort_entire_phrase(phrase)
                abort_specific_phrases = None
                return True, ""
            else:
                print("Matching abort specific phrase but not timestamps")
                print(abort_specific_phrases)
                print(current_phrase, start, end)
        abort_specific_phrases = None

    if ts_threshold != 0:
        # Start of phrase is before timestamp threshold
        start = getattr(words[0], "start", None) or phrase.get("_ts", ts_threshold)
        delta = ts_threshold - start
        ts_threshold = 0
        if delta > 0:
            actions.user.debug(f"Aborted phrase: {delta:.2f}s")
            abort_entire_phrase(phrase)
            return True, ""

    if words[-1] in abort_phrases:
        abort_phrase = words[-1]
        abort_phrase_substitute = abort_phrases[abort_phrase]
        # Update phrase that is used by analyze phrase
        phrase["phrase"] = phrase["phrase"][-1:]

        # Updating the sequence is what actually aborts the command we don't want to do.
        # You could just set an empty list: phrase["parsed"]._sequence = []
        # Unfortunately that will not work with analyze phrase since our command history won't be updated.

        phrase["parsed"]._sequence = [
            get_capture(phrase, abort_phrase, abort_phrase_substitute),
        ]

        if len(words) > 1:
            return True, f"... {abort_phrase_substitute}"
        return True, abort_phrase_substitute

    return False, current_phrase


def abort_entire_phrase(phrase: Phrase):
    phrase["phrase"] = []
    if "parsed" in phrase:
        phrase["parsed"]._sequence = []


def get_capture(
    phrase: Phrase,
    abort_phrase: str,
    abort_phrase_substitute: str,
) -> Capture:
    # Last capture in sequence is actually cancel, just reused that one.
    capture = phrase["parsed"]._sequence[-1]
    if abort_phrase == str(capture):
        return capture

    # Last capture is not a cancel command. Probably a back anchored phrase.
    # eg: "say hello cancel"
    # The way to get around this is to actually construct the cancel capture.

    # {user.abort_phrase}$ encoded to talon command
    name = "___lbuser_2eabort_5fphrase_rb_ra__"
    sequence = [DecodeWord(abort_phrase_substitute)]
    vmc = VMCapture(name=name, data=sequence)
    return Capture(vm_capture=vmc, sequence=sequence, mapping={})


def intersects(t1_start: float, t1_end: float, t2_start: float, t2_end: float) -> bool:
    """Returns true if the two time intervals intersects"""
    return (t1_start <= t2_start <= t1_end) or (t2_start <= t1_start <= t2_end)
