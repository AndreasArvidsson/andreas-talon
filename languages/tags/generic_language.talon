tag: user.generic_language
-

# ----- Selection statements -----
make if:                    user.code_if()
make elif:                  user.code_elif()
make else:                  user.code_else()
make switch:                user.code_switch()
make case:                  user.code_case()
make default:               user.code_default()
make try:                   user.code_try()
make catch:                 user.code_catch()
make try catch:             user.code_try_catch()

# ----- Iteration statements -----
make for [loop]:            user.code_for()
make while [loop]:          user.code_while()
make do while [loop]:       user.code_do_while()
make for each [loop]:       user.code_foreach()

# ----- Miscellaneous statements -----
make true:                  user.code_true()
make false:                 user.code_false()
make break:                 user.code_break()
make continue:              user.code_continue()
make return:                user.code_return()
make link [<user.text>]:    user.code_link(text or "")

# ----- Print statements -----
make print:                 user.code_print("")
format string:              user.code_format_string()

# ----- Insert language specific text and snippets -----
make <user.code_inserts>:   "{code_inserts}"
make {user.code_snippet}:   user.insert_snippet("{code_snippet}")

# ----- Class statement -----
{user.code_class_modifier}* class <user.text>$:
    user.code_class_wrapper(text, code_class_modifier_list or "")

# ----- Function statement -----
{user.code_function_modifier}* (function| funk) <user.text>$:
    user.code_function_wrapper(text, code_function_modifier_list or "")
{user.code_function_modifier}* method <user.text>$:
    user.code_method_wrapper(text, code_function_modifier_list or "")

(function| funk) main:      user.code_function_main()

# ----- Constructor statement -----
{user.code_function_modifier}* (function| funk) constructor:
    user.code_constructor_wrapper(code_function_modifier_list or "")

# ----- Variable statement -----
var {user.code_variable_modifier}* [{user.code_data_type}] <user.text>:
    user.code_variable_wrapper(text, code_variable_modifier_list or "", false, code_data_type or "")
var {user.code_variable_modifier}* [{user.code_data_type}] <user.text> equals:
    user.code_variable_wrapper(text, code_variable_modifier_list or "", true, code_data_type or "")

# ----- Insert data type -----
type {user.code_data_type}: "{code_data_type}"
is type {user.code_data_type}:
    user.code_insert_type_annotation(code_data_type)
is type <user.text>:
    format = user.code_get_class_format()
    data_type = user.format_text(text, format)
    user.code_insert_type_annotation(data_type)
returns type {user.code_data_type}:
    user.code_insert_return_type(code_data_type)

# ----- Function call -----
call {user.code_function}:  user.code_call_function(code_function)
