from talon import Module, Context, speech_system

# from talon.engines.vosk import VoskEngine
from talon.engines.webspeech import WebSpeechEngine

speech_system.add_engine(
    WebSpeechEngine(),
)

# speech_system.add_engine(
#     VoskEngine(model="vosk-model-small-sv-rhasspy-0.15", language="sv_SE"),
# )

mod = Module()
mod.tag("swedish", "Use voice engine for Swedish")

# Context for Swedish dictation
ctx_sv = Context()
ctx_sv.matches = r"""
tag: user.swedish
"""

ctx_sv.settings = {
    "speech.engine": "webspeech",
    # "speech.engine": "vosk",
    "speech.language": "sv_SE",
}
