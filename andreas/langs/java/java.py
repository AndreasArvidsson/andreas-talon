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
        insert("if () {\n\n}\n")
        key("up:3 end left:3")
    def code_elif():
        insert("else if () {\n\n}\n")
        key("up:3 end left:3")
    def code_else():
        insert("else {\n\n}\n")
        key("up:2")
    def code_switch():
        insert("switch () {\n\n}\n")
        key("up:3 end left:3")
    def code_case(): insert("case ")
    def code_default(): insert("default:")
    
    # Iteration statements
    def code_for():
        insert("for (int i = 0; i < .size(); ++i) {\n\n}\n")
        key("up:3 home right:20")
    def code_while():
        insert("while () {\n\n}\n")
        key("up:3 end left:3")
    def code_do_while():
        insert("do {\n\n} while ();\n")
        key("up end left:2")
    def code_foreach():
        insert("for (final  : ) {\n\n}\n")
        key("up:3 end left:6")
    
    # Miscellaneous statements
    def code_break(): insert("break;")
    def code_true(): insert("true")
    def code_false(): insert("false")
    def code_continue(): insert("continue;")
    def code_return(): insert("return")
    def code_comment(): insert("// ")
    def code_block_comment():
        insert("/*\n\n*/")
        key("up")
    def code_print(text: str):
        if text:
            insert('System.out.println("{}");\n'.format(
                actions.user.formatted_text(text, "CAPITALIZE_FIRST_WORD")
            ))
        else:
            insert("System.out.println();")
            key("left:2")

    # Class statement
    def code_class(access_modifier: str or None, name: str):
        text = f"class {name} {{\n\n\n}}"
        if access_modifier:
            text = f"{access_modifier} {text}"
        else:
            text = f"public {text}"
        insert(text)
        key("up tab")

    # Constructor statement
    def code_constructor(access_modifier: str or None):
        name = get_constructor_name()
        if not name:
            return
        if access_modifier:
            text = f"{access_modifier} {name}"
        else:
            text = f"public {name}"
        insert(f"{text}() {{\n\n}}\n")
        key("up:3 end left:3")

    # Function statement
    def code_function(access_modifier: str or None, name: str):
        text = f"void {name}() {{}}\n"
        if access_modifier:
            text = f"{access_modifier} {text}"
        insert(text)
        key("up end left enter up end left:3")

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
    actions.edit.select_none()
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
