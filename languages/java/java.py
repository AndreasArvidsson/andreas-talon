from talon import Module, Context, actions

mod = Module()
ctx = Context()

ctx.matches = r"""
code.language: java
"""

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
ctx.lists["self.code_class_modifier"] = {*access_modifiers, *abstract, *final}
ctx.lists["self.code_function_modifier"] = {
    *access_modifiers,
    *abstract,
    *final,
    *static,
}
ctx.lists["self.code_variable_modifier"] = {*access_modifiers, *final, *static}
code_data_type_simple = {
    "int",
    "long",
    "short",
    "char",
    "byte",
    "float",
    "double",
    "String",
    "Map",
    "List",
    "Set",
    "Object",
}
ctx.lists["self.code_data_type"] = {
    **{t: t for t in code_data_type_simple},
    "bool": "boolean",
    "array list": "ArrayList",
    "hash set": "HashSet",
    "hash map": "HashMap",
}

ctx.lists["self.code_function"] = {"toString"}
ctx.lists["self.code_insert"] = {
    **{k: f"{k} " for k in all_keywords},
    "null": "null",
    "this": "this",
    "import": "import ",
    "new": "new ",
    "extends": "extends ",
    "implements": "implements ",
    "class": "class ",
    "void": "void ",
    "throw": "throw ",
    "instance of": " instanceof ",
}


@ctx.action_class("user")
class UserActions:
    # Math operators
    def op_exp():
        actions.skip()

    # Miscellaneous statements
    def insert_arrow():
        actions.insert(" -> ")

    # Class declaration
    def code_class(name: str, modifiers: list[str]):
        actions.user.code_insert_snippet(
            "classDeclaration",
            {"name": name, "modifiers": get_modifiers(modifiers)},
        )

    # Constructor declaration
    def code_constructor(modifiers: list[str]):
        name = actions.user.vscode_get("andreas.getClassName")
        if not name:
            return
        actions.user.code_insert_snippet(
            "constructorDeclaration",
            {"name": name, "modifiers": get_modifiers(modifiers)},
        )

    # Function declaration
    def code_function(name: str, modifiers: list[str]):
        actions.user.code_insert_snippet(
            "functionDeclaration",
            {"name": name, "modifiers": get_modifiers(modifiers)},
        )

    def code_function_main():
        actions.user.code_insert_snippet(
            "functionDeclaration",
            {
                "name": "main",
                "modifiers": "public static",
                "1": "String[] args",
            },
        )

    # Variable declaration
    def code_variable(
        name: str, modifiers: list[str], assign: bool, data_type: str = None
    ):
        text = name
        if data_type:
            text = f"{data_type} {text}"
        if modifiers:
            text = f"{' '.join(modifiers)} {text}"
        if assign:
            text += " = "
        actions.insert(text)


def get_modifiers(modifiers: list[str]):
    if modifiers:
        return " ".join(modifiers)
    else:
        return "public"
