tag: user.code_generic_language
-
tag(): user.code_inserts
tag(): user.code_call_function

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

# ----- Insert symbol -----
symbol {user.code_symbol}:  insert(code_symbol)
