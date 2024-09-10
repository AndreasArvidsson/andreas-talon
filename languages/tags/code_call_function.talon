tag: user.code_call_function
-

calling {user.code_call_function}:
    user.code_call_function(code_call_function)

calling <user.text_code>:
    format = user.code_get_variable_format()
    text_code = user.format_text(text_code, format)
    user.code_call_function(text_code)
