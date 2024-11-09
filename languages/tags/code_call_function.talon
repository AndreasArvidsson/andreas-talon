tag: user.code_call_function
-

calling {user.code_call_function}:
    user.code_call_function(code_call_function)

calling <user.code_id>:
    format = user.code_get_variable_format()
    text = user.format_text(code_id, format)
    user.code_call_function(text)
