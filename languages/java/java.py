from talon import Module, Context, actions
from ..tags.code_operators import CodeOperators

mod = Module()
ctx = Context()

ctx.matches = r"""
code.language: java
"""

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
    is_equal         = " == ",
    is_not_equal     = " != ",
    is_less          = " < ",
    is_greater       = " > ",
    is_less_equal    = " <= ",
    is_greater_equal = " >= ",
    is_not           = "!",
    is_null          = " == null",
    is_not_null      = " != null",
    op_and           = " && ",
    op_or            = " || ",
)

access_modifiers = {
    "public",
    "private",
    "protected",
}

abstract = {"abstract"}
final = {"final"}
static = {"static"}

all_keywords = {
    *access_modifiers,
    *abstract,
    *final,
    *static,
}

ctx.lists["user.code_variable_modifier"] = {  # pyright: ignore[reportArgumentType]
    *access_modifiers,
    *final,
    *static,
}

code_data_type_simple = {
    "int",
    "long",
    "short",
    "char",
    "byte",
    "float",
    "double",
    "String",
    "boolean",
    "Object",
    "void",
    "Map",
    "List",
    "Set",
}

ctx.lists["user.code_data_type"] = {
    **{t: t for t in code_data_type_simple},
    "bool"       : "boolean",
    "bite"       : "byte",
}

ctx.lists["user.code_collection_type"] = {
    "list"            : "List",
    "set"             : "Set",
    "map"             : "Map",
    "array list"      : "ArrayList",
    "a ray list"      : "ArrayList",
    "hash set"        : "HashSet",
    "hash map"        : "HashMap",
    "linked hash map" : "LinkedHashMap"
}

ctx.lists["user.code_call_function"] = {
    "to string"  : "toString",
    "equals"     : "equals",
}

ctx.lists["user.code_keyword"] = {
    **{k: f"{k} " for k in all_keywords},
    "true"          : "true",
    "false"         : "false",
    "null"          : "null",
    "this"          : "this",
    "import"        : "import ",
    "new"           : "new ",
    "return"        : "return ",
    "extends"       : "extends ",
    "implements"    : "implements ",
    "class"         : "class ",
    "void"          : "void ",
    "throw"         : "throw ",
    "instance of"   : " instanceof ",
    "continue"      : "continue;",
    "break"         : "break;",
    "yield"         : "yield ",
    "var"           : "var ",

    "nullable"      : "@Nullable ",
    "null marked"   : "@NullMarked",
    "inject"        : "@Inject",
    "context"       : "@Context",
    "get"           : "@GET",
    "post"          : "@POST",
    "put"           : "@PUT",
    "patch"         : "@PATCH",
    "delete"        : "@DELETE",
    "path"          : "@Path",
    "roles allowed" : "@RolesAllowed",
    "consumes"      : "@Consumes",
    "produces"      : "@Produces",
    "json creator"  : "@JsonCreator",
    "json property" : "@JsonProperty",
    "json schema"   : "@JsonSchema",
}

# fmt: on


@ctx.action_class("user")
class UserActions:
    def code_constructor():
        actions.user.code_constructor_with_class_name()

    @staticmethod
    def code_variable(assign: bool, modifiers: list[str], data_type: str, name: str):
        snippet = ""
        if modifiers:
            snippet = f"{' '.join(modifiers)} "
            if "final" in modifiers:
                assign = True
        if not data_type and not name:
            snippet += "$1"
        else:
            snippet += f"{data_type or '$1'} {name or '$1'}"
        if assign:
            snippet += " = $0"
        actions.user.insert_snippet(snippet)
