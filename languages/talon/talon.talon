code.language: talon
-
tag(): user.code_operators
tag(): user.code_comments
tag(): user.code_inserts
tag(): user.code_call_function

settings():
    user.code_function_formatter = "SNAKE_CASE"
    user.code_variable_formatter = "SNAKE_CASE"

# Context requirements
require {user.code_talon_context}: "{code_talon_context}"
