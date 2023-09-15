from talon import Module, actions

mod = Module()

mod.tag("code_call_function")

mod.list("code_call_function", "Names of functions to call")


@mod.action_class
class Action:
    def code_call_function(name: str):
        """Call function <name>"""
        actions.user.code_insert_snippet_by_name("functionCall", {"name": name})
