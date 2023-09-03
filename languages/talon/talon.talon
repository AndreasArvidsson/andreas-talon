code.language: talon
-
tag(): user.code_operators
tag(): user.code_comments
tag(): user.code_inserts
tag(): user.code_call_function

# Context requirements
require {user.code_talon_context}: "{code_talon_context}"

# Generic
snip command:               user.code_insert_snippet("voiceCommandDeclaration")
