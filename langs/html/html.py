from talon import Module, Context, actions

mod = Module()
ctx = Context()

ctx.matches = r"""
mode: user.html
mode: user.auto_lang
and code.language: html
mode: user.auto_lang
and code.language: javascript
"""

tag_names_list = {
    "html", "head", "body", "header", "footer", "main", "aside",
    "div", "span", "table", "template", "script", "nav",
    "button", "input", "textarea", "select", "option", "form",
    "label", "Link", "hr"
}

tag_names = {
    "anchor":           "a",
    "table headers":    "thead",
    "table body":       "tbody",
    "table foot":   "   tfoot",
    "table row":        "tr",
    "table head":       "th",
    "table cell":       "td",
    "olist":            "ol",
    "unlist":           "ul",
    "list item":        "li",
    "image":            "img",
    "head one":         "h1",
    "head two":         "h2",
    "head three":       "h3",
    "head four":        "h4",
    "head five":        "h5",
    "head six":         "h6",
    "break":            "br"
}
tag_names.update(dict(zip(tag_names_list, tag_names_list)))

mod.list("code_tag", desc="Predefined tag names")
ctx.lists["self.code_tag"] = tag_names

tags = []

@mod.action_class
class user_actions:
    def code_push_tag_name(name: str):
        """Push tag name"""
        tags.append(name)

    def code_close_tag():
        """Close last tag"""
        if len(tags) < 1:
            return
        name = tags.pop()
        actions.insert(f"</{name}>" )
