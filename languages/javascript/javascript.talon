tag: user.javascript
-
tag(): user.generic_language
tag(): user.c_common
tag(): user.operators
tag(): user.comments

# ----- JavaScript additional -----

(op | is) in:               " in "

convert to arrow:           user.arrowify_line()

make arrow function <user.text>:
    format = user.code_get_function_format()
    name = user.format_text(text, format)
    user.insert_snippet("const {name} = ($1) => {{\n$0\n}}")
