from talon import Module, Context
from urllib.parse import quote_plus
import webbrowser

mod = Module()


@mod.action_class
class Actions:
    def search_with_search_engine(search_text: str):
        """Search a search engine for given text"""
        if is_url(search_text):
            url = search_text
        else:
            url = "https://duckduckgo.com/?q=" + quote_plus(search_text)
        webbrowser.open(url)


def is_url(text: str):
    return (text.startswith("https://")
            or text.startswith("http://")
            or text.startswith("www."))
