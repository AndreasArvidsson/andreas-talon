tag: user.generic_language
-
tag(): user.operators

# ----- Selection statements -----
make if:                      user.code_if()
make elif:                    user.code_elif()
make else:                    user.code_else()
make switch:                  user.code_switch()
make case:                    user.code_case()
make default:                 user.code_default()

# ----- Iteration statements -----
make for loop:                user.code_for()
make while loop:              user.code_while()
make do while [loop]:         user.code_do_while()
make foreach [loop]:          user.code_foreach()

# ----- Miscellaneous statements -----
make true:                    user.code_true()
make false:                   user.code_false()
make break:                   user.code_break()
make continue:                user.code_continue()
make return:                  user.code_return()

make print:                   user.code_print("")
make print <user.text>$:
    text = user.format_text(text, "CAPITALIZE_FIRST_WORD")
    user.code_print(text)
make new line:                "\\n"
make {user.code_statement}:   "{code_statement}"

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

function main:                 user.code_main_function()

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

type {user.code_data_type}:    "{code_data_type}"

# ----- Function call -----
call {user.code_function}:     user.code_call_function(code_function)

# ----- Member access -----
{user.code_member_op} {user.code_member}:
    user.code_member_access(code_member_op, code_member)