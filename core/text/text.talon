# Formatted prose phrase: "sentence hello there" -> Hello there
{user.formatter_prose} <user.prose>$:
    user.insert_formatted(prose, formatter_prose)
{user.formatter_prose} <user.prose> {user.phrase_ender}:
    user.insert_formatted(prose, formatter_prose)
    "{phrase_ender}"

# Formatted code phrase: "camel hello there" -> helloThere
{user.formatter_code} <user.text_code>:
    user.insert_formatted(text_code, formatter_code)
{user.formatter_code} <user.text_code> {user.phrase_ender}:
    user.insert_formatted(text_code, formatter_code)
    "{phrase_ender}"

# Only words, no symbols or numbers
escape <user.phrase>$:      "{phrase}"
escape <user.phrase> over:  "{phrase}"

# Single word: "word up" => up, "proud up" => Up
{user.formatter_word} <user.word>:
    user.insert_formatted(word, formatter_word)
# Single abbreviated word. "proud brief app" => App
{user.formatter_word} <user.abbreviation>:
    user.insert_formatted(abbreviation, formatter_word)
# Abbreviated word without formatter: "breif application" => app, "breif app" => app
<user.abbreviation>:        "{abbreviation}"

# Easy access to specific Swedish phrases
swe {user.swedish_phrase}:  "{swedish_phrase}"
{user.formatter_word} swe {user.swedish_phrase}:
    user.insert_formatted(swedish_phrase, formatter_word)
{user.formatter_prose} swe <user.prose>$:
    translated = user.translate_english_to_swedish(prose)
    user.insert_formatted(translated, formatter_prose)
swe <user.prose>$:
    translated = user.translate_english_to_swedish(prose)
    insert(translated)

# Upper case characters
ship <user.letters> [over]:
    user.insert_formatted(letters, "ALL_UPPERCASE")
