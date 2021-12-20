from talon import Module, Context, actions

mod = Module()
ctx = Context()

mod.list("delimiters_spaced", desc="List of delimiters with trailing white space")
ctx.lists["self.delimiters_spaced"] = {
    "spam":     ",",
    "stacker":  ":",
    "period":   ".",
    "bullet":   "*",
}

mod.list("delimiter_pair", desc="List of matching pair delimiters")
matching_pairs = {
    "round":    ["(", ")"],
    "index":    ["[", "]"],
    "diamond":  ["<", ">"],
    "curly":    ["{", "}"],
    "twin":     ["'", "'"],
    "string":   ['"', '"'],
    "skis":     ['`', '`'],
}
ctx.lists["self.delimiter_pair"] = matching_pairs.keys()

matching_pairs_wrap = {
    "quad":     ['"', '"'],
    "square":   ["[", "]"],
    "angle":    ["<", ">"],
    "void":     [" ", " "],
}

matching_pairs_all = {
    **matching_pairs,
    **matching_pairs_wrap,
}

mod.list("delimiter_pair_wrap", desc="List of matching pair delimiters use specifically for wrapping")
ctx.lists["self.delimiter_pair_wrap"] = matching_pairs_all.keys()


@mod.action_class
class Actions:
    def delimiters_pair_insert(pair_name: str):
        """Insert matching pair delimiters"""
        pair = matching_pairs_all[pair_name]
        actions.user.insert_snippet(f"{pair[0]}$0{pair[1]}")

    def delimiters_pair_wrap_selection(pair_name: str):
        """Wrap selection with matching pair delimiters"""
        selected = actions.edit.selected_text()
        if selected:
            pair = matching_pairs_all[pair_name]
            actions.insert(f"{pair[0]}{selected}{pair[1]}")
