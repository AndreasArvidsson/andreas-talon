from talon import Module, actions, speech_system
from talon.grammar import Phrase

mod = Module()

phrase_stack = []

def on_pre_phrase(d):  phrase_stack.append(d)
def on_post_phrase(d): phrase_stack.pop()

speech_system.register("pre:phrase", on_pre_phrase)
speech_system.register("post:phrase", on_post_phrase)

@mod.action_class
class Actions: 
    def rephrase(phrase: Phrase):
        """Rerun phrase"""
        current_phrase = phrase_stack[-1]
        ts = current_phrase["_ts"]
        start = phrase.words[0].start - ts
        end   = phrase.words[-1].end - ts
        samples = current_phrase["samples"]
        pstart  = int(start * 16_000)
        pend    = int(end   * 16_000)
        samples = samples[pstart:pend]

        speech_system._on_audio_frame(samples)
