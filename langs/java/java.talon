mode: command
and mode: user.java

mode: command
and mode: user.auto_lang
and code.language: java
-
tag(): user.generic_language
tag(): user.comments

# ----- Java additional -----

make arrow function:
    "() -> {\n\n}"
    key(up:2 end left:6)

new {user.code_data_type}:
    "new {code_data_type}();"
    key(left:2)

new <user.variable_name>:
    format = user.code_get_class_format()
    name = user.format_text(variable_name, format)
    user.history_add_phrase(name)
    "new {name}();"
    key(left:2)

(op | is) null:       " == null"
(op | is) not null:   " != null"