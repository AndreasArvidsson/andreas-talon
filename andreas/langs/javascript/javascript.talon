mode: user.javascript
mode: user.auto_lang
and code.language: javascript
-
tag(): user.generic_language

# ----- JavaScript additional -----

arrow function <user.variable_name>:
    format = user.code_get_function_format()
    name = user.formatted_text(variable_name, format)
    user.history_add_phrase(name)
    "const {name} = () => {{\n\n}}\n"
    key(up:3 end left:6)

convert to arrow: user.arrowify_line()

state for in loop:
    "for (const i in ) {\n\n}\n"
    key(up:3 end left:3)

method <user.words>:
    format = user.code_get_function_format()
    name = user.formatted_text(words, format)
    user.history_add_phrase(name)
    "{name}() {{\n\n}}\n"
    key("up:3 end left:3")

state arrow function:
    "() => {\n\n}"
    key(up:2 end left:6)
