from talon import actions

input_raw = "why? and it's nice!"
input_raw_numbers = "why? and it's nice 123!"

fixtures_format = [
    # Simple formatters
    ["NOOP", input_raw, input_raw],
    ["TRAILING_PADDING", input_raw, f"{input_raw} "],
    ["ALL_CAPS", input_raw, input_raw.upper()],
    ["ALL_LOWERCASE", input_raw, input_raw.lower()],
    ["DOUBLE_QUOTED_STRING", input_raw, '"why? and it\'s nice!"'],
    ["SINGLE_QUOTED_STRING", input_raw, "'why? and it's nice!'"],
    # Splitting formatters
    ["CAPITALIZE_ALL_WORDS", input_raw, "Why? And It's Nice!"],
    ["CAPITALIZE_FIRST_WORD", input_raw, "Why? and it's nice!"],
    # Delimited formatters
    ["CAMEL_CASE", input_raw, "why?andItsNice!"],
    ["PASCAL_CASE", input_raw, "Why?AndItsNice!"],
    ["SNAKE_CASE", input_raw, "why?and_its_nice!"],
    ["ALL_CAPS_SNAKE_CASE", input_raw, "WHY?AND_ITS_NICE!"],
    ["DASH_SEPARATED", input_raw, "why?and-its-nice!"],
    ["DOT_SEPARATED", input_raw, "why?and.its.nice!"],
    ["SLASH_SEPARATED", input_raw, "why?and/its/nice!"],
    ["DOUBLE_UNDERSCORE", input_raw, "why?and__its__nice!"],
    ["DOUBLE_COLON_SEPARATED", input_raw, "why?and::its::nice!"],
    ["NO_SPACES", input_raw, "why?anditsnice!"],
    # More tests with special characters
    ["Numbers camel", "CAMEL_CASE", input_raw_numbers, "why?andItsNice123!"],
    ["Numbers snake", "SNAKE_CASE", input_raw_numbers, "why?and_its_nice_123!"],
]

input_snake = "hello_there.my_ip_address_2_x_3"
input_camel = "helloThere.myIPAddress2x3"
output_raw = "hello there my ip address 2 x 3"

fixtures_reformat = [
    ["COMMA_SEPARATED", input_raw, "why?, and, it's, nice!"],
    ["Unformat snake", "REMOVE_FORMATTING", input_snake, output_raw],
    ["Unformat camel", "REMOVE_FORMATTING", input_camel, output_raw],
    ["Snake to camel", "CAMEL_CASE", input_snake, "helloThereMyIpAddress2x3"],
    ["Camel to snake", "SNAKE_CASE", input_camel, "hello_there_my_ip_address_2_x_3"],
]


def test(fixture, callback):
    formatter = fixture[-3]
    input = fixture[-2]
    expected = fixture[-1]
    found = callback(input, formatter)
    actions.user.assert_equals(expected, found)


# actions.user.start_test(
#     "format", fixtures_format, lambda f: test(f, actions.user.format_text)
# )
# actions.user.start_test(
#     "reformat", fixtures_reformat, lambda f: test(f, actions.user.reformat_text)
# )


# # Test unformat_text
# tests = {
#     "say": "hello, I'm ip address 2!",
#     "sentence": "Hello, I'm ip address 2!",
#     "allcaps": "HELLO, I'M IP ADDRESS 2!",
#     "camel": "helloThereIPAddressA2a2",
#     "Pascal": "HelloThereIPAddressA2a2",
#     "snake": "hello_there_ip_address_2",
#     "kebab": "hello-there-ip-address-2",
#     "packed": "hello::there::ip::address::2",
#     "dotted": "hello.there.ip.address.2",
#     "slasher": "hello/there/ip/address/2",
#     "dunder": "hello__there__ip_address__2"
# }
# for key, value in tests.items():
#     text = actions.user.unformat_text(value)
#     print(f"{key.ljust(15)}{value.ljust(35)}{text}")
