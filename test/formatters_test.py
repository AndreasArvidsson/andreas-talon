from talon import actions

input_raw = "why? and. It's nice!"
input_raw_numbers = "why? and. It's nice 123.0!"
import_unicode = "Hej på dig åäö"

fixtures_format = [
    # Simple formatters
    ["NO_FORMAT", input_raw, input_raw],
    ["TRAILING_SPACE", input_raw, f"{input_raw} "],
    ["ALL_UPPERCASE", input_raw, input_raw.upper()],
    ["ALL_LOWERCASE", input_raw, input_raw.lower()],
    ["DOUBLE_QUOTED_STRING", input_raw, '"why? and. It\'s nice!"'],
    ["SINGLE_QUOTED_STRING", input_raw, "'why? and. It's nice!'"],
    ["NO_SPACES", "why?\nand.\tIt's  nice`!", "why?and.Itsnice!"],
    # Splitting formatters
    ["CAPITALIZE_ALL_WORDS", input_raw, "Why? And. It's Nice!"],
    ["CAPITALIZE_FIRST_WORD", input_raw, "Why? and. It's nice!"],
    # Delimited formatters
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
    ["Numbers camel", "CAMEL_CASE", input_raw_numbers, "whyAnd.itsNice123.0"],
    ["Numbers snake", "SNAKE_CASE", input_raw_numbers, "why_and.its_nice_123.0"],
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
    ["COMMA_SEPARATED", input_raw, "why?, and., It's, nice!"],
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
    ["Upper to sentence", "CAPITALIZE_FIRST_WORD", "HELLO WORLD", "Hello world"],
    ["Upper to title", "CAPITALIZE_ALL_WORDS", "HELLO WORLD", "Hello World"],
    ["Snake to upper", "ALL_UPPERCASE", "hello_world", "HELLO_WORLD"],
    ["Constant to lower", "ALL_LOWERCASE", "HELLO_WORLD", "hello_world"],
    ["Twin to snake", "SNAKE_CASE", "'hello world'", "'hello_world'"],
    ["Quad to snake", "SNAKE_CASE", '"hello world"', '"hello_world"'],
    ["Docstring to snake", "SNAKE_CASE", '"""hello world"""', '"""hello_world"""'],
    [
        "Preserve whitespace",
        "CAPITALIZE_ALL_WORDS",
        "\thello\nworld ",
        "\tHello\nWorld ",
    ],
    [
        "Sentence to snake",
        "SNAKE_CASE",
        "foo shortterm bar iPhone baz",
        "foo_shortterm_bar_iphone_baz",
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
