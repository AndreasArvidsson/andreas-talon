# ----- Matching delimiter pairs -----
<user.delimiter_pair>:      user.delimiters_pair_insert(delimiter_pair)

# Wrap selection with delimiter pair
<user.delimiter_pair> this:
    user.delimiters_pair_wrap_selection(delimiter_pair)

<user.delimiter_pair> last:
    user.history_select_last_phrase()
    user.delimiters_pair_wrap_selection(delimiter_pair)

<user.delimiter_pair> word:
    edit.select_word()
    user.delimiters_pair_wrap_selection(delimiter_pair)

# ----- Delimiters with trailing space -----
{user.delimiters_spaced}:   "{delimiters_spaced} "