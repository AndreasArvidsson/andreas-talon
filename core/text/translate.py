import json
import time
from urllib.parse import urlencode
from urllib.request import urlopen
from talon import Module, actions

mod = Module()


@mod.action_class
class Actions:
    @staticmethod
    def translate_english_to_swedish(text: str) -> str:
        """Translate english text to swedish"""
        return translate("en", "sv", text)

    @staticmethod
    def translate_swedish_to_english(text: str) -> str:
        """Translate swedish text to english"""
        return translate("sv", "en", text)


def translate(source_lang: str, target_lang: str, text: str) -> str:
    t1 = time.perf_counter()
    translated = google_translate(source_lang, target_lang, text)
    t2 = time.perf_counter()
    actions.user.debug(
        f"Translated {len(text)} characters in {round((t2 - t1) * 1000)}ms"
    )
    return translated


def google_translate(source_lang: str, target_lang: str, text: str) -> str:
    query = urlencode(
        {
            # The "client" parameter is set to "gtx" to indicate that this request is coming from a Google Translate client.
            "client": "gtx",
            # The "dt" parameter is set to "t" to specify that we want the translated text in the response.
            "dt": "t",
            # The "sl" parameter is set to the source language code (e.g., "en" for English) to specify the language of the input text.
            "sl": source_lang,
            # The "tl" parameter is set to the target language code (e.g., "sv" for Swedish) to specify the language we want the text translated into.
            "tl": target_lang,
            # The "q" parameter is set to the text we want to translate.
            "q": text,
        }
    )

    url = f"https://translate.googleapis.com/translate_a/single?{query}"

    with urlopen(url, timeout=3) as response:
        data = json.loads(response.read().decode("utf-8"))

    return "".join(part[0] for part in data[0] if part[0])
