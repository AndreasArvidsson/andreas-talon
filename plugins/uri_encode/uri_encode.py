from talon import Module, actions
from urllib import parse

mod = Module()


@mod.action_class
class Actions:
    def uri_encode(text: str) -> str:
        """Encodes a string to be used in a URI"""
        return parse.quote(text)

    def uri_encode_selection():
        """Encodes selection to be used in a URI"""
        text = actions.edit.selected_text()
        encoded = actions.user.uri_encode(text)
        actions.insert(encoded)

    def uri_decode(text: str) -> str:
        """Decodes a string from a URI"""
        return parse.unquote(text)

    def uri_decode_selection():
        """Decodes selection from a URI"""
        text = actions.edit.selected_text()
        decoded = actions.user.uri_decode(text)
        actions.insert(decoded)
