tag: user.code_generic_language
-

tag(): user.code_keywords
tag(): user.code_call_function

# ----- Constructor statement -----
snip constructor:
    user.code_constructor()

# ----- Variable statement -----
# Requires modifier, optional datatype
snip {user.code_variable_modifier}+ [{user.code_data_type}] [<user.code_id>]:
    user.code_variable_wrapper(true, code_variable_modifier_list or "", code_data_type or "", code_id or "")
# Requires datatype, optional modifier
snip {user.code_variable_modifier}* {user.code_data_type} [<user.code_id>]:
    user.code_variable_wrapper(true, code_variable_modifier_list or "", code_data_type or "", code_id or "")

# ----- Insert data type -----
type <user.code_data_type>: "{code_data_type}"
is type <user.code_data_type>:
    user.code_insert_type_annotation(code_data_type)
returns type <user.code_data_type>:
    user.code_insert_return_type(code_data_type)
