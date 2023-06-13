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
    "skis":     ['`', '`'],
}

matching_pairs_all = {
    **matching_pairs,
    "void":     [" ", " "],
}

# fmt: on

mod.list("delimiter_pair", desc="List of matching pair delimiters")
ctx.lists["self.delimiter_pair"] = matching_pairs.keys()

mod.list(
    "delimiter_pair_wrap",
    desc="List of matching pair delimiters use specifically for wrapping",
)
ctx.lists["self.delimiter_pair_wrap"] = matching_pairs_all.keys()


@mod.action_class
class Actions:
    def delimiters_pair_insert_by_name(pair_name: str):
        """Insert matching delimiters pair <pair_name>"""
        [left, right] = matching_pairs_all[pair_name]
        actions.user.delimiters_pair_insert(left, right)

    def delimiters_pair_insert(left: str, right: str, middle: str = ""):
        """Insert delimiter pair <left> and <right> with interior <middle>"""
        actions.insert(f"{left}{middle}{right}")
        for _ in right:
            actions.edit.left()

    def delimiters_pair_wrap_selection(pair_name: str):
        """Wrap selection with matching delimiter pair <pair_name>"""
        [left, right] = matching_pairs_all[pair_name]
        actions.user.delimiters_pair_wrap_selection_with(left, right)

    def delimiters_pair_wrap_selection_with(left: str, right: str):
        """Wrap selection with delimiters <left> and <right>"""
        selected = actions.edit.selected_text()
        actions.user.delimiters_pair_insert(left, right, selected)
