from talon import speech_system

# from talon.engines.vosk import VoskEngine
from talon.engines.webspeech import WebSpeechEngine

# Google chrome. http://localhost:7419
speech_system.add_engine(
    WebSpeechEngine(),
)

# speech_system.add_engine(
#     VoskEngine(model="vosk-model-small-sv-rhasspy-0.15", language="sv_SE"),
# )
