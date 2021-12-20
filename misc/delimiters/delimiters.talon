# ----- Matching delimiter pairs -----
{user.delimiter_pair}:      user.delimiters_pair_insert_by_name(delimiter_pair)

{user.delimiter_pair_wrap} wrap word:
    edit.select_word()
    user.delimiters_pair_wrap_selection(delimiter_pair_wrap)

# ----- Delimiters with trailing space -----
{user.delimiters_spaced}:   "{delimiters_spaced} "