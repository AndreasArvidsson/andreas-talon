from talon import Module, Context, actions

mod = Module()
ctx = Context()

ctx.matches = r"""
code.language: talon
"""

ctx.lists["self.code_call_function"] = {
    "key",
    "insert",
}
ctx.lists["self.code_insert"] = {
    "true": "true",
    "false": "false",
    "tag": "tag(): ",
}

mod.list("code_talon_context", "List of Talon context matches")
ctx.lists["self.code_talon_context"] = {
    "win": "os: windows\n",
    "mac": "os: mac\n",
    "linux": "os: linux\n",
    "title": "title: ",
    "app": "app: ",
    "tag": "tag: ",
}


@ctx.action_class("user")
class UserActions:
    # Assignment operator
    def op_assign():
        actions.insert(" = ")

    # Math operators
    def op_sub():
        actions.insert(" - ")

    def op_sub_assign():
        actions.insert(" -= ")

    def op_add():
        actions.insert(" + ")

    def op_add_assign():
        actions.insert(" += ")

    def op_mult():
        actions.insert(" * ")

    def op_mult_assign():
        actions.insert(" *= ")

    def op_div():
        actions.insert(" / ")

    def op_div_assign():
        actions.insert(" /= ")

    def op_mod():
        actions.insert(" % ")

    def op_mod_assign():
        actions.insert(" %= ")

    def op_exp():
        actions.insert(" ** ")

    # Boolean operators
    def op_and():
        actions.insert("and ")

    def op_or():
        actions.insert(" or ")

    def op_equal():
        actions.insert(" == ")

    def op_not_equal():
        actions.insert(" != ")

    def op_less():
        actions.insert(" < ")

    def op_greater():
        actions.insert(" > ")

    def op_less_or_eq():
        actions.insert(" <= ")

    def op_greater_or_eq():
        actions.insert(" >= ")

    def op_not():
        actions.insert("not ")
