code.language: markdown
-
tag(): user.code_generic_language

snip link [<user.prose>]:   user.code_markdown_link(prose or "")

# Formatter wrappers
{user.markdown_pair} this:
    user.delimiters_pair_wrap_selection_with(markdown_pair, markdown_pair)
{user.markdown_pair} token:
    edit.select_word()
    user.delimiters_pair_wrap_selection_with(markdown_pair, markdown_pair)
{user.markdown_pair} line:
    edit.select_line()
    user.delimiters_pair_wrap_selection_with(markdown_pair, markdown_pair)
