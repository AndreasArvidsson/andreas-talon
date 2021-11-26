tag: user.javascript
-
tag(): user.html
tag(): user.generic_language
tag(): user.operators
tag(): user.comments

# ----- JavaScript additional -----

arrow function <user.variable_name>:
    format = user.code_get_function_format()
    name = user.format_text(variable_name, format)
    user.history_add_phrase(name)
    "const {name} = () => {{\n\n}}\n"
    key(up:3 end left:6)

convert to arrow:   user.arrowify_line()

make for in loop:
    "for (const i in ) {\n\n}\n"
    key(up:3 end left:3)

method <user.variable_name>:
    format = user.code_get_function_format()
    name = user.format_text(variable_name, format)
    user.history_add_phrase(name)
    "{name}() {{\n\n}}\n"
    key("up:3 end left:3")

make arrow function:
    "() => {\n\n}"
    key(up:2 end left:6)