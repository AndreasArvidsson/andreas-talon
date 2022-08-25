from talon import Module, Context, actions

mod = Module()

ctx = Context()
ctx.matches = r"""
tag: user.html
"""

tag_names_list = {
    "html",
    "head",
    "body",
    "header",
    "footer",
    "main",
    "aside",
    "div",
    "span",
    "table",
    "template",
    "script",
    "nav",
    "button",
    "input",
    "textarea",
    "select",
    "option",
    "form",
    "label",
    "Link",
    "hr",
}

# fmt: off
tag_names = {
    "anchor":           "a",
    "table headers":    "thead",
    "table body":       "tbody",
    "table foot":       "tfoot",
    "table row":        "tr",
    "table head":       "th",
    "table cell":       "td",
    "olist":            "ol",
    "unlist":           "ul",
    "list item":        "li",
    "image":            "img",
    "harp one":         "h1",
    "harp two":         "h2",
    "harp three":       "h3",
    "harp four":        "h4",
    "harp five":        "h5",
    "harp six":         "h6",
    "break":            "br"
}
# fmt: on

mod.list("code_tag", desc="Predefined tag names")
ctx.lists["self.code_tag"] = {
    **{n: n for n in tag_names_list},
    **tag_names,
}


tags = []


@mod.action_class
class Actions:
    def code_push_tag_name(name: str):
        """Push tag name"""
        tags.append(name)

    def code_close_tag():
        """Close last tag"""
        if len(tags) < 1:
            return
        name = tags.pop()
        actions.insert(f"</{name}>")


@ctx.action_class("user")
class UserActions:
    # Comments
    def comments_insert(text: str = ""):
        actions.user.insert_snippet(f"<!-- {text}$0 -->")

    def comments_insert_block(text: str = ""):
        actions.user.comments_insert(text)
