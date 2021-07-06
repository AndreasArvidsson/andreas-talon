tag: user.generic_language
-
tag(): user.operators

# ----- Selection statements -----
state if:                      user.code_if()
state elif:                    user.code_elif()
state else:                    user.code_else()
state switch:                  user.code_switch()
state case:                    user.code_case()
state default:                 user.code_default()

# ----- Iteration statements -----
state for loop:                user.code_for()
state while loop:              user.code_while()
state do while [loop]:         user.code_do_while()
state foreach [loop]:          user.code_foreach()

# ----- Miscellaneous statements -----
state true:                    user.code_true()
state false:                   user.code_false()
state break:                   user.code_break()
state continue:                user.code_continue()
state return:                  user.code_return()
state comment <user.text>:
    user.code_comment()
    text = user.format_text(text, "CAPITALIZE_FIRST_WORD")
    "{text}"
state comment:                 user.code_comment()
state block comment:           user.code_block_comment()
state print [<user.text>]:     
    text = user.format_text(text or "", "CAPITALIZE_FIRST_WORD")
    user.code_print(text)
state new line:                "\\n"
state {user.code_statement}:   "{code_statement}"

# ----- Class statement -----
class [{user.code_access_modifier}] <user.variable_name>:
    format = user.code_get_class_format()
    name = user.format_text(variable_name, format)
    user.history_add_phrase(name)
    user.code_class(code_access_modifier or "", name)

# ----- Constructor statement -----
constructor [{user.code_access_modifier}]:
    user.code_constructor(code_access_modifier or "")

# ----- Function statement -----
function [{user.code_access_modifier}] <user.variable_name>:
    format = user.code_get_function_format()
    name = user.format_text(variable_name, format)
    user.history_add_phrase(name)
    user.code_function(code_access_modifier or "", name)

# ----- Variable statement -----
var [{user.code_access_modifier}] [{user.code_data_type}] <user.variable_name>:
    format = user.code_get_variable_format()
    name = user.format_text(variable_name, format)
    user.history_add_phrase(name)
    user.code_variable(code_access_modifier or "", code_data_type or "", name, "")

var [{user.code_access_modifier}] [{user.code_data_type}] <user.variable_name> (equals | equal):
    format = user.code_get_variable_format()
    name = user.format_text(variable_name, format)
    user.history_add_phrase(name)
    user.code_variable(code_access_modifier or "", code_data_type or "", name, "ASSIGN")

type {user.code_data_type}:    "{code_data_type} "

# ----- Function call -----
call {user.code_function}:     user.code_call_function(code_function)

call <user.variable_name>:
    format = user.code_get_function_format()
    name = user.format_text(variable_name, format)
    user.history_add_phrase(name)
    user.code_call_function(name)

# ----- Member access -----
{user.code_member_op} {user.code_member}:
    user.code_member_access(code_member_op, code_member)
{user.code_member_op} <user.variable_name>:
    user.code_member_access(code_member_op, variable_name)