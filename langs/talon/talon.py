from talon import Module, Context, actions
insert = actions.insert

mod = Module()
ctx = Context()

ctx.matches = r"""
mode: user.talon
mode: user.auto_lang
and code.language: talon
"""

@ctx.action_class("user")
class UserActions:
    # Assignment operator
    def op_assign():            insert(" = ")

    # Math operators
    def op_sub():               insert(" - ")
    def op_sub_assign():        insert(" -= ")
    def op_add():               insert(" + ")
    def op_add_assign():        insert(" += ")
    def op_mult():              insert(" * ")
    def op_mult_assign():       insert(" *= ")
    def op_div():               insert(" / ")
    def op_div_assign():        insert(" /= ")
    def op_mod():               insert(" % ")
    def op_mod_assign():        insert(" %= ")
    def op_exp():               insert(" ** ")

    # Boolean operators
    def op_and():               insert("and ")
    def op_or():                insert(" or ")
    def op_equal():             insert(" == ")
    def op_not_equal():         insert(" != ")
    def op_less():              insert(" < ")
    def op_greater():           insert(" > ")
    def op_less_or_eq():        insert(" <= ")
    def op_greater_or_eq():     insert(" >= ")
    def op_not():               insert("not ")
