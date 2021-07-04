from talon import Module, Context, actions
from user.util import merge
import re
insert = actions.insert
key = actions.key

mod = Module()
ctx = Context()

ctx.matches = r"""
mode: user.java
mode: user.auto_lang
"""

ctx.lists["self.code_data_type"] = merge(
    {
        "int", "long", "short", "char", "byte", "bool", "float", "double", "String",
        "Map", "List", "Set"
    },
    {
        "array list":       "ArrayList",
        "hash set":         "HashSet",
        "hash map":         "HashMap"
    }
)
ctx.lists["self.code_member_op"] = {
    "dot": "."
}
ctx.lists["self.code_function"] = {
    "to string":    "toString"
}
ctx.lists["self.code_member"] = {
    "length"
}
ctx.lists["self.code_statement"] = {
    "import":               "import ",
    "null":                 "null",
    "arrow":                " -> ",
    "this":                 "this",
    "this dot":             "this.",
    "new":                  "new ",
    "public":               "public ",
    "private":              "private "
}
ctx.lists["self.code_access_modifier"] = {
    "public", "private", "protected"
}


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
    def op_exp():               actions.skip()
    
    # Boolean operators
    def op_and():               insert(" && ")
    def op_or():                insert(" || ")
    def op_equal():             insert(" == ")
    def op_not_equal():         insert(" != ")
    def op_less():              insert(" < ")
    def op_greater():           insert(" > ")
    def op_less_or_eq():        insert(" <= ")
    def op_greater_or_eq():     insert(" >= ")
    def op_not():               insert("!")
    
    # Selection statements
    def code_if():
        snip_func("if")
    def code_elif():
        snip_func("else if")
    def code_else():
        insert("else {}")
        key("left enter")
    def code_switch():
        snip_func("switch")
    def code_case(): insert("case ")
    def code_default(): insert("default:")
    
    # Iteration statements
    def code_for():
        insert("for (int i = 0; i < .size(); ++i) {}")
        key("left enter up home right:20")
    def code_while():
        snip_func("while")
    def code_do_while():
        insert("do {} while ();")
        key("left:11 enter down end left:2")
    def code_foreach():
        insert("for (final  : ) {}")
        key("left enter up end left:6")
    
    # Miscellaneous statements
    def code_break(): insert("break;")
    def code_true(): insert("true")
    def code_false(): insert("false")
    def code_continue(): insert("continue;")
    def code_return(): insert("return")
    def code_comment(): insert("// ")
    def code_block_comment():
        insert("/**/")
        key("left:2 enter:2 up")
    def code_print():
        insert("System.out.println();")
        key("left:2")

    # Class statement
    def code_class(access_modifier: str or None, name: str):
        text = f"class {name} {{}}"
        if access_modifier:
            text = f"{access_modifier} {text}"
        else:
            text = f"public {text}"
        insert(text)
        key("left enter")

    # Constructor statement
    def code_constructor(access_modifier: str or None):
        name = get_constructor_name()
        if not name:
            return
        if access_modifier:
            name = f"{access_modifier} {name}"
        else:
            name = f"public {name}"
        snip_func(name)

    # Function statement
    def code_function(access_modifier: str or None, name: str):
        name = f"void {name}"
        if access_modifier:
            text = f"{access_modifier} {name}"
        snip_func(name)

    # Variable declaration
    def code_variable(access_modifier: str or None, data_type: str or None, name: str, assign: str or None):
        text = name
        if data_type:
            text = f"{data_type} {text}"
        if access_modifier:
            text = f"{access_modifier} {text}"
        if assign:
            text = text + " = "
        insert(text)

    # Function call
    def code_call_function(name: str):
        insert(f"{name}()")
        key("left")
    
    # Member access
    def code_member_access(operator: str, name: str):
        insert(f"{operator}{name}")

    # Formatting getters
    def code_get_class_format() -> str:     return "PASCAL_CASE"
    def code_get_function_format() -> str:  return "CAMEL_CASE"
    def code_get_variable_format() -> str:  return "CAMEL_CASE"

def get_constructor_name():
    """Code constructor"""
    actions.edit.extend_file_start()
    text = actions.edit.selected_text()
    actions.edit.right()
    index1 = text.rfind("class")
    if index1 < 0:
        return
    index1 += len("class")
    index2 = text.find("{", index1)                
    if index2 < 0:
        return
    name = text[index1 : index2]
    # Strip parameterized type
    name = re.sub(r"<\w*>", "", name).strip()
    # Strip implements and extends
    name = name.split(" ")[0]
    return name.strip()

def snip_func(name):
    insert(f"{name} () {{}}")
    key("left enter up end left:3")
