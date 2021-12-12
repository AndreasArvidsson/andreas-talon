tag: user.javascript
-
tag(): user.generic_language
tag(): user.operators
tag(): user.comments

# ----- JavaScript additional -----

make arrow function <user.variable_name>:
    format = user.code_get_function_format()
    name = user.format_text(variable_name, format)
    user.history_add_phrase(name)
    user.insert_snippet("const {name} = ($1) => {{\n$0\n}}")

convert to arrow:   user.arrowify_line()

make for in loop:
    user.insert_snippet("for (const i in $1) {{\n$0\n}}")

method <user.variable_name>:
    format = user.code_get_function_format()
    name = user.format_text(variable_name, format)
    user.history_add_phrase(name)
    user.insert_snippet("{name}($1) {{\n$0\n}}")

make arrow function:
    user.insert_snippet("($1) => {\n$0\n}")