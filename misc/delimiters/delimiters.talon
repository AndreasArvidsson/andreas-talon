# Matching delimiter pairs: "round" => ()
{user.delimiter_pair}:
    user.delimiters_pair_insert_by_name(delimiter_pair)

# String phrase: "string hello" => "hello"
string [<user.text>] [over]:
    user.delimiters_pair_insert('"', '"', text or "")
