# linux: `TALON_HOME/bin/pip install -U deep-translator`
# win:   `TALON_HOME/venv/3.11/Scripts/pip.bat install -U deep-translator`

from talon import Module, actions
from deep_translator import GoogleTranslator
import time

en_to_sv = GoogleTranslator(source="en", target="sv")


mod = Module()


@mod.action_class
class Actions:
    def translate_english_to_swedish(english_text: str) -> str:
        """Translate english text to swedish"""
        t1 = time.perf_counter()
        translated = en_to_sv.translate(english_text)
        t2 = time.perf_counter()
        actions.user.debug(
            f"Translated {len(english_text)} characters in {round((t2-t1)*100)}ms"
        )
        return translated
