tag: user.generic_language
-

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
make {user.code_statement}:
    "{code_statement}"
make {user.code_class_modifier}:
    "{code_class_modifier}"
make {user.code_function_modifier}:
    "{code_function_modifier}"
make {user.code_variable_modifier}:
    "{code_variable_modifier}"

make print:                   user.code_print("")
make print <user.text>$:
    text = user.format_text(text, "CAPITALIZE_FIRST_WORD")
    user.code_print(text)

format string:                user.code_format_string()

# ----- Class statement -----
{user.code_class_modifier}* class <user.variable_name>:
    user.code_class_wrapper(variable_name, code_class_modifier_list or "")

# ----- Function statement -----
{user.code_function_modifier}* function <user.variable_name>:
    user.code_function_wrapper(variable_name, code_function_modifier_list or "")

function main:                user.code_function_main()

# ----- Constructor statement -----
{user.code_function_modifier}* function constructor:
    user.code_constructor_wrapper(code_function_modifier_list or "")

# ----- Variable statement -----
var {user.code_variable_modifier}* [{user.code_data_type}] <user.variable_name>:
    user.code_variable_wrapper(variable_name, code_variable_modifier_list or "", 0, code_data_type or "")
var {user.code_variable_modifier}* [{user.code_data_type}] <user.variable_name> equals:
    user.code_variable_wrapper(variable_name, code_variable_modifier_list or "", 1, code_data_type or "")

# ----- Insert data type -----
type {user.code_data_type}:   "{code_data_type}"

# ----- Function call -----
call {user.code_function}:    user.code_call_function(code_function)