# ----- Matching delimiter pairs -----
<user.delimiter_pair>:      user.delimiters_pair_insert(delimiter_pair)

<user.delimiter_pair> wrap word:
    edit.select_word()
    user.delimiters_pair_wrap_selection(delimiter_pair)

# ----- Delimiters with trailing space -----
{user.delimiters_spaced}:   "{delimiters_spaced} "