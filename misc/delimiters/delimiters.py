from talon import Module, Context, actions

mod = Module()
ctx = Context()

# fmt: off

matching_pairs = {
    "round":    ["(", ")"],
    "index":    ["[", "]"],
    "diamond":  ["<", ">"],
    "curly":    ["{", "}"],
    "twin":     ["'", "'"],
    "quad":     ['"', '"'],
    "string":   ['"', '"'],
    "skis":     ['`', '`'],
}

matching_pairs_all = {
    **matching_pairs,
    "void":     [" ", " "],
}

# fmt: on

ctx.lists["self.delimiter_pair"] = matching_pairs.keys()
mod.list("delimiter_pair", desc="List of matching pair delimiters")

mod.list(
    "delimiter_pair_wrap",
    desc="List of matching pair delimiters use specifically for wrapping",
)
ctx.lists["self.delimiter_pair_wrap"] = matching_pairs_all.keys()


@mod.action_class
class Actions:
    def delimiters_pair_insert_by_name(pair_name: str):
        """Insert matching pair delimiters by name"""
        pair = matching_pairs_all[pair_name]
        actions.user.delimiters_pair_insert(pair[0], pair[1])

    def delimiters_pair_insert(left: str, right: str):
        """Insert matching pair delimiters"""
        actions.insert(f"{left}{right}")
        actions.edit.left()

    def delimiters_pair_wrap_selection(pair_name: str):
        """Wrap selection with matching pair delimiters"""
        selected = actions.edit.selected_text()
        if selected:
            pair = matching_pairs_all[pair_name]
            actions.insert(f"{pair[0]}{selected}{pair[1]}")
