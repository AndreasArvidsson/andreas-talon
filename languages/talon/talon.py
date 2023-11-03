from talon import Module, Context
from ..tags.code_operators import CodeOperators

mod = Module()
ctx = Context()

ctx.matches = r"""
code.language: talon
"""

mod.list("code_talon_context", "List of Talon context matches")

# fmt: off
ctx.lists["user.code_operator"] = CodeOperators(
    op_assign        = " = ",
    op_sub           = " - ",
    op_sub_assign    = " -= ",
    op_add           = " + ",
    op_add_assign    = " += ",
    op_mult          = " * ",
    op_mult_assign   = " *= ",
    op_div           = " / ",
    op_div_assign    = " /= ",
    op_mod           = " % ",
    op_mod_assign    = " %= ",
    op_pow           = " ** ",
    is_equal         = " == ",
    is_not_equal     = " != ",
    is_less          = " < ",
    is_greater       = " > ",
    is_less_equal    = " <= ",
    is_greater_equal = " >= ",   
    is_not           = "not ",
    is_null          = " is None",
    is_not_null      = " is not None",
    is_in            = " in ",
    op_and           = " and ",
    op_or            = " or ",
)
ctx.lists["user.code_call_function"] = {
    "key",
    "insert",
}
ctx.lists["user.code_insert"] = {
    "true"  : "true",
    "false" : "false",
    "tag"   : "tag(): ",
}
ctx.lists["user.code_talon_context"] = {
    "win"   : "os: windows\n",
    "mac"   : "os: mac\n",
    "linux" : "os: linux\n",
    "title" : "title: ",
    "app"   : "app: ",
    "tag"   : "tag: ",
}
# fmt: on
