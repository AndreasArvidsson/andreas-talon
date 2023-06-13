tag: user.markdown
-

# Formatter wrappers
{user.markdown_pair} this:
    user.delimiters_pair_wrap_selection_with(markdown_pair, markdown_pair)
{user.markdown_pair} token:
    edit.select_word()
    user.delimiters_pair_wrap_selection_with(markdown_pair, markdown_pair)
{user.markdown_pair} line:
    edit.select_line()
    user.delimiters_pair_wrap_selection_with(markdown_pair, markdown_pair)
