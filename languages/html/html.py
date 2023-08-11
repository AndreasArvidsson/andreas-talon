from talon import Module, Context, actions

mod = Module()

ctx = Context()
ctx.matches = r"""
code.language: html
code.language: javascriptreact
code.language: typescriptreact
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
        """Push tag <name>"""
        tags.append(name)

    def code_close_tag():
        """Close last tag"""
        if len(tags) < 1:
            return
        name = tags.pop()
        actions.insert(f"</{name}>")

    def code_insert_element(name: str):
        """Insert element <name>"""
        actions.user.code_insert_snippet("element", {"name": name})

    def code_insert_attribute(name: str):
        """Insert attribute <name>"""
        actions.user.code_insert_snippet("attribute", {"name": f" {name}"})
