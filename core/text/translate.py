# linux: `TALON_HOME/bin/pip install -U deep-translator`
# win:   `TALON_HOME/venv/3.11/Scripts/pip.bat install -U deep-translator`

from talon import Module, actions
from deep_translator import GoogleTranslator
import time

en_to_sv = GoogleTranslator(source="en", target="sv")
sv_to_en = GoogleTranslator(source="sv", target="en")


mod = Module()


@mod.action_class
class Actions:
    def translate_english_to_swedish(text: str) -> str:
        """Translate english text to swedish"""
        return translate(en_to_sv, text)

    def translate_swedish_to_english(text: str) -> str:
        """Translate swedish text to english"""
        return translate(sv_to_en, text)


def translate(translator: GoogleTranslator, text: str) -> str:
    t1 = time.perf_counter()
    translated = translator.translate(text)
    t2 = time.perf_counter()
    actions.user.debug(f"Translated {len(text)} characters in {round((t2-t1)*100)}ms")
    return translated
