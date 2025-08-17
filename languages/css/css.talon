code.language: css
code.language: scss
-

settings():
    user.code_function_formatter = "DASH_SEPARATED"
    user.code_variable_formatter = "DASH_SEPARATED"

# ----- Variable statement -----
snip var [<user.code_id>]:
    user.code_variable_wrapper(true, "", "", code_id or "")
