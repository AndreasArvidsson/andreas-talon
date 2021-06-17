mode: user.java
mode: user.auto_lang
and code.language: java
-
tag(): user.generic_language

# ----- Java additional -----

state main:
    "public static void main(String[] args) {\n\n}\n"
    key(up:2)

state arrow function:
    "() -> {\n\n}"
    key(up:2 end left:6)

new {user.code_data_types}: "new {code_data_types}();"
new <user.variable_name>:
    format = user.code_get_class_format()
    name = user.formatted_text(variable_name, format)
    user.history_add_phrase(name)
    "new {name}();"