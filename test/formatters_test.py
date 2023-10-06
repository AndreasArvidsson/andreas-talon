from talon import actions

input_raw = "why? and. It's nice!"
input_raw_symbols = "why? and. It's nice 123.0!,hello"
import_unicode = "Hej på dig åäö"

fixtures_format = [
    # Special formatters
    ["TRAILING_SPACE", input_raw, f"{input_raw} "],
    ["DOUBLE_QUOTED_STRING", input_raw, f'"{input_raw}"'],
    ["SINGLE_QUOTED_STRING", input_raw, f"'{input_raw}'"],
    # Prose formatters
    ["KEEP_FORMAT", input_raw, input_raw],
    ["ALL_UPPERCASE", input_raw, input_raw.upper()],
    ["ALL_LOWERCASE", input_raw, input_raw.lower()],
    ["TITLE_CASE", input_raw, "Why? And. It's Nice!"],
    ["TITLE_CASE", "abc    abc", "Abc    Abc"],
    ["TITLE_CASE", "\tabc\nabc ", "\tAbc\nAbc "],
    ["TITLE_CASE", "aBc aBc aBc", "aBc aBc aBc"],
    ["TITLE_CASE", "and and and", "And and And"],
    ["TITLE_CASE", "and. and and", "And. And And"],
    ["TITLE_CASE", "abc and-and-and abc", "Abc And-and-And Abc"],
    ["TITLE_CASE", "1st 2nd 3rd", "1st 2nd 3rd"],
    ["SENTENCE", input_raw, "Why? and. It's nice!"],
    ["SENTENCE", "aBc abc", "aBc abc"],
    # Code formatters
    ["NO_SPACES", "why?\nand.\tIt's  nice`!", "whyand.itsnice"],
    ["CAMEL_CASE", input_raw, "whyAnd.itsNice"],
    ["PASCAL_CASE", input_raw, "WhyAnd.ItsNice"],
    ["SNAKE_CASE", input_raw, "why_and.its_nice"],
    ["ALL_UPPERCASE,SNAKE_CASE", input_raw, "WHY_AND.ITS_NICE"],
    ["DASH_SEPARATED", input_raw, "why-and.its-nice"],
    ["DOT_SEPARATED", input_raw, "why.and.its.nice"],
    ["SLASH_SEPARATED", input_raw, "why/and.its/nice"],
    ["DOUBLE_UNDERSCORE", input_raw, "why__and.its__nice"],
    ["DOUBLE_COLON_SEPARATED", input_raw, "why::and.its::nice"],
    # Symbols
    ["Numbers camel", "CAMEL_CASE", input_raw_symbols, "whyAnd.itsNice123.0, hello"],
    ["Numbers snake", "SNAKE_CASE", input_raw_symbols, "why_and.its_nice_123.0, hello"],
    # Unicode characters
    ["Unicode camel", "CAMEL_CASE", import_unicode, "hejPåDigÅäö"],
    ["Unicode snake", "SNAKE_CASE", import_unicode, "hej_på_dig_åäö"],
]

input_camel = "helloThere.myIPAddress2x3"
input_snake = "hello_there.my_ip_address_2_x_3"
input_camel_unicode = "hejPåDigÅäö"
input_snake_unicode = "hej_på_dig_åäö"
output_raw = "hello there my ip address 2 x 3"
output_raw_unicode = "hej på dig åäö"

fixtures_reformat = [
    ["CAPITALIZE_FIRST_WORD", input_raw, "Why? and. It's nice!"],
    ["CAPITALIZE_FIRST_WORD", "aBc abc", "Abc abc"],
    ["COMMA_SEPARATED", input_raw, "why?, and., It's, nice!"],
    ["COMMA_SEPARATED", "a b  c", "a, b, c"],
    ["Unformat snake", "REMOVE_FORMATTING", input_snake, output_raw],
    [
        "Unformat unicode snake",
        "REMOVE_FORMATTING",
        input_snake_unicode,
        output_raw_unicode,
    ],
    ["Unformat camel", "REMOVE_FORMATTING", input_camel, output_raw],
    [
        "Unformat unicode camel",
        "REMOVE_FORMATTING",
        input_camel_unicode,
        output_raw_unicode,
    ],
    ["Snake to camel", "CAMEL_CASE", input_snake, "helloThereMyIpAddress2x3"],
    ["Camel to snake", "SNAKE_CASE", input_camel, "hello_there_my_ip_address_2_x_3"],
    ["Camel to snake unicode", "SNAKE_CASE", input_camel_unicode, input_snake_unicode],
    ["Snake to camel unicode", "CAMEL_CASE", input_snake_unicode, input_camel_unicode],
    ["Upper to sentence", "SENTENCE", "HELLO WORLD", "Hello world"],
    ["Upper to title", "TITLE_CASE", "HELLO WORLD", "Hello World"],
    ["Snake to upper", "ALL_UPPERCASE", "hello_world", "HELLO_WORLD"],
    ["Constant to lower", "ALL_LOWERCASE", "HELLO_WORLD", "hello_world"],
    ["Twin to snake", "SNAKE_CASE", "'hello world'", "'hello_world'"],
    ["Quad to snake", "SNAKE_CASE", '"hello world"', '"hello_world"'],
    ["Docstring to snake", "SNAKE_CASE", '"""hello world"""', '"""hello_world"""'],
    ["Append camel case", "CAMEL_CASE", "set userAccounts", "setUserAccounts"],
    [
        "Sentence to snake",
        "SNAKE_CASE",
        "foo shortterm bar iPhone baz",
        "foo_shortterm_bar_i_phone_baz",
    ],
]


def test(fixture, callback):
    formatter = fixture[-3]
    input = fixture[-2]
    expected = fixture[-1]
    found = callback(input, formatter)
    actions.user.assert_equals(expected, found)


def test_formatters():
    actions.user.test_run_suite(
        "format", fixtures_format, lambda f: test(f, actions.user.format_text)
    )
    actions.user.test_run_suite(
        "reformat", fixtures_reformat, lambda f: test(f, actions.user.reformat_text)
    )
