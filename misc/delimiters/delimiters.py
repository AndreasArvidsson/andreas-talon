from talon import Module, Context, actions

mod = Module()
ctx = Context()

mod.list("delimiters_spaced", desc="List of delimiters with trailing white space")
ctx.lists["self.delimiters_spaced"] = {
    "spam":     ",",
    "col gap":  ":",
    "period":   ".",
}

mod.list("delimiter_pair", desc="List of matching pair delimiters")
matching_pairs = {
    "round":    ["(", ")"],
    "index":    ["[", "]"],
    "diamond":  ["<", ">"],
    "curly":    ["{", "}"],
    "twin":     ["'", "'"],
    "quad":     ['"', '"'],
    "skis":     ['`', '`'],
}
matching_pairs["string"] = matching_pairs["quad"]
ctx.lists["self.delimiter_pair"] = matching_pairs.keys()


@mod.capture(rule="{user.delimiter_pair}")
def delimiter_pair(m) -> list[str]:
    return matching_pairs[m.delimiter_pair]


@mod.action_class
class Actions:
    def delimiters_pair_insert(pair: list[str]):
        """Insert matching pair delimiters"""
        actions.insert(pair[0] + pair[1])
        actions.edit.left()

    def delimiters_pair_wrap_selection(pair: list[str]):
        """Wrap selection with matching pair delimiters"""
        selection = actions.edit.selected_text()
        actions.insert(pair[0])
        actions.insert(selection)
        actions.insert(pair[1])
