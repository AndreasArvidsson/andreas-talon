tag: user.code_variables
-

# Requires modifier, optional datatype
snip {user.code_variable_modifier}+ [{user.code_data_type}] [<user.code_id>]:
    user.code_variable_wrapper(true, code_variable_modifier_list or "", code_data_type or "", code_id or "")
# Requires datatype, optional modifier
snip {user.code_variable_modifier}* {user.code_data_type} [<user.code_id>]:
    user.code_variable_wrapper(true, code_variable_modifier_list or "", code_data_type or "", code_id or "")
