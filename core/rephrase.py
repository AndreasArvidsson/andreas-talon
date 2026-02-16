from talon import Module, speech_system, cron
from talon.grammar import Phrase

mod = Module()

phrase_stack = []


def on_pre_phrase(d):
    phrase_stack.append(d)


def on_post_phrase(_):
    if phrase_stack:
        phrase_stack.pop()


speech_system.register("pre:phrase", on_pre_phrase)
speech_system.register("post:phrase", on_post_phrase)


@mod.action_class
class Actions:
    def rephrase(phrase: Phrase, run_async: bool = False):
        """Re-evaluate and run phrase"""
        if not phrase_stack:
            return

        try:
            current_phrase = phrase_stack[-1]
            ts = current_phrase["_ts"]
            start_ts = getattr(phrase.words[0], "start", None)
            end_ts = getattr(phrase.words[-1], "end", None)
            if start_ts is None or end_ts is None:
                return
            start = start_ts - ts
            end = end_ts - ts
            samples = current_phrase["samples"]
            pstart = int(start * 16_000)
            pend = int(end * 16_000)
            if pstart >= pend:
                return
            samples = samples[pstart:pend]
        except Exception:
            return

        if run_async:
            cron.after("0ms", lambda: speech_system._on_audio_frame(samples))
        else:
            speech_system._on_audio_frame(samples)
