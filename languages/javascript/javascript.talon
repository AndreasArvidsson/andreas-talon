code.language: javascript
code.language: typescript
code.language: javascriptreact
code.language: typescriptreact
-
tag(): user.code_generic_language
tag(): user.code_operators
tag(): user.code_comments

settings():
    user.code_class_formatter = "PASCAL_CASE"
    user.code_function_formatter = "CAMEL_CASE"
    user.code_variable_formatter = "CAMEL_CASE"

# ----- JavaScript additional -----

convert to arrow:           user.js_arrowify_line()

snip arrow funk <user.prose>:
    user.js_arrow_function(prose)
