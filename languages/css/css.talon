code.language: css
code.language: scss
-

settings():
    user.code_function_formatter = "DASH_SEPARATED"
    user.code_variable_formatter = "DASH_SEPARATED"

# ----- Variable statement -----
var <user.prose>:
    user.code_variable_wrapper(prose, "", false, "")
var <user.prose> equals:
    user.code_variable_wrapper(prose, "", true, "")
