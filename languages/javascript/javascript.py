from talon import Module, Context, actions
from ..tags.code_operators import CodeOperators

mod = Module()
ctx = Context()

ctx.matches = r"""
code.language: javascript
code.language: typescript
code.language: javascriptreact
code.language: typescriptreact
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
    op_pow           = " ** ",
    is_equal         = " === ",
    is_not_equal     = " !== ",
    is_less          = " < ",
    is_greater       = " > ",
    is_less_equal    = " <= ",
    is_greater_equal = " >= ",
    is_not           = "!",
    is_null          = " == null",
    is_not_null      = " != null",
    op_in            = " in ",
    op_and           = " && ",
    op_or            = " || ",
    is_in            = " in ",
)

ctx.lists["user.code_class_modifier"] = {}
ctx.lists["user.code_function_modifier"] = {}
ctx.lists["user.code_data_type"] = {}
ctx.lists["user.code_collection_type"] = {}

ctx.lists["user.code_variable_modifier"] = {
    "const",
    "let",
}

ctx.lists["user.code_call_function"] = {
    "forEach",
    "map",
    "flatMap",
    "filter",
    "reduce",
    "sort",
    "find",
    "includes",
    "indexOf",
    "join",
    "require",
}

javascript_inserts = {
    "true":         "true",
    "false":        "false",
    "null":         "null",
    "undefined":    "undefined",
    "this":         "this",
    "from":         " from ",
    "import":       "import ",
    "export":       "export ",
    "default":      "default ",
    "extends":      " extends ",
    "implements":   " implements ",
    "abstract":     "abstract ",
    "return":       "return ",
    "a sync":       "async ",
    "await":        "await ",
    "function":     "function ",
    "spread":       "...",
    "new":          "new ",
    "const":        "const ",
    "let":          "let ",
    "throw":        "throw ",
    "static":       "static ",
    "get":          "get ",
    "set":          "set ",
    "nullish":      " ?? ",
    "instance of":  " instanceof ",
    "type of":      "typeof ",
    "yield":        "yield ",
    "delete":       "delete ",
    "void":         "void ",
    "continue":     "continue;",
    "break":        "break;",
}

ctx.lists["user.code_insert"] = javascript_inserts

# fmt: on


@ctx.action_class("user")
class UserActions:
    # Class statement
    def code_class(name: str, modifiers: list[str]):
        actions.user.insert_snippet_by_name("classDeclaration", {"name": name})

    # Constructor statement
    def code_constructor(modifiers: list[str]):
        actions.user.insert_snippet_by_name("constructorDeclaration")

    # Function statement
    def code_function(name: str, modifiers: list[str]):
        actions.user.insert_snippet_by_name("functionDeclaration", {"name": name})

    def code_method(name: str, modifiers: list[str]):
        if modifiers:
            name = f"{''.join(modifiers)} {name}"
        actions.user.insert_snippet_by_name("methodDeclaration", {"name": name})

    # Variable statement
    def code_variable(
        name: str, modifiers: list[str], assign: bool, data_type: str = None
    ):
        text = name
        if modifiers:
            text = f"{' '.join(modifiers)} {text}"
            if "const" in modifiers:
                assign = True
        if data_type:
            text = f"{text}: {data_type}"
        if assign:
            text += " = "
        actions.insert(text)

    # Formatting getters
    def code_get_class_format() -> str:
        return "PASCAL_CASE"

    def code_get_function_format() -> str:
        return "CAMEL_CASE"

    def code_get_variable_format() -> str:
        return "CAMEL_CASE"


@mod.action_class
class Actions:
    def js_arrowify_line():
        """Arrowify line"""
        actions.edit.select_line()
        text = actions.edit.selected_text()
        if "function" in text:
            text = text.replace("function ", "")
        text = f"const {text}"
        text = text.replace("(", " = (")
        text = text.replace(")", ") =>")
        actions.insert(text)

    def js_arrow_function(name: str):
        """Insert arrow function"""
        format = actions.user.code_get_function_format()
        name = actions.user.format_text(name, format)
        actions.user.insert_snippet_by_name("namedLambdaExpression", {"1": name})
