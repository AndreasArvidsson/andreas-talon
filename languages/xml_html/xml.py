from talon import Module, actions

mod = Module()

mod.list("code_tag", "Predefined tag names")


@mod.action_class
class Actions:
    def code_close_tag():
        """Close last open tag"""
        name = actions.user.code_get_open_tag_name()
        if name:
            actions.insert(f"</{name}>")

    def code_insert_element(name: str):
        """Insert element <name>"""
        actions.user.insert_snippet_by_name("element", {"name": name})

    def code_insert_attribute(name: str):
        """Insert attribute <name>"""
        actions.user.insert_snippet_by_name("attribute", {"name": f" {name}"})
