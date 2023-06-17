# Formatted prose phrase: "sentence hello there" -> Hello there
{user.formatter_prose} <user.prose>$:
    user.insert_formatted(prose, formatter_prose)
{user.formatter_prose} <user.prose> {user.phrase_ender}:
    user.insert_formatted("{prose}{phrase_ender}", formatter_prose)

# Formatted code phrase: "camel hello there" -> helloThere
{user.formatter_code} <user.text_code> [over]:
    user.insert_formatted(text_code, formatter_code)
strict {user.formatter_code} <user.text_code>$:
    user.insert_formatted(text_code, formatter_code)

# Only words, no symbols or numbers
escape <user.words>$:       "{words}"
escape <user.words> over:   "{words}"

# Single word: "word up" => up, "proud up" => Up
{user.formatter_word} <user.word>:
    user.insert_formatted(word, formatter_word)
# Single abbreviated word. "proud brief app" => App
{user.formatter_word} <self.abbreviation>:
    user.insert_formatted(abbreviation, formatter_word)
# Single homophone word
{user.formatter_word} <user.ordinals_small> <user.word>:
    homophone = user.homophones_get_by_number(word, ordinals_small)
    user.insert_formatted(homophone, formatter_word)
# Abbreviated word without formatter: "breif application" => app, "breif app" => app
<user.abbreviation>:        "{abbreviation}"

# Easy access to specific Swedish phrases
swe {user.swedish_phrase}:  "{swedish_phrase}"
{user.formatter_word} swe {user.swedish_phrase}:
    user.insert_formatted(swedish_phrase, formatter_word)

# Upper case characters
ship <user.letters> [over]:
    user.insert_formatted(letters, "ALL_CAPS")
