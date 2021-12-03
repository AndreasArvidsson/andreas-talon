from talon import Context, actions, Module
key = actions.key
insert = actions.insert
skip = actions.skip
ctx = Context()
mod = Module()

mod.apps.visual_studio = """
os: windows
and app.name: Microsoft Visual Studio 2019
os: windows
and app.name: devenv.exe
"""

ctx.matches = r"""
app: visual_studio
"""

ctx.tags = ["user.ide"]


@ctx.action_class("win")
class win_actions:
    def filename():
        title = actions.win.title()
        result = title.split(" - ")[0]
        if "." in result:
            return result
        return ""


@ctx.action_class("app")
class AppActions:
    # ----- Tabs -----
    def tab_previous():     key("ctrl-alt-pageup")
    def tab_next():         key("ctrl-alt-pagedown")


@ctx.action_class("user")
class UserActions:
    def tab_final():        key("ctrl-alt-end")

    def format_document():  key("ctrl-k ctrl-d")
    def format_selection(): key("ctrl-k ctrl-f")

    # ----- Navigation -----
    def go_to_declaration(): key("ctrl-alt-f12")
    def go_to_definition():  key("f12")
    def go_to_references():  skip()

    # ----- Find -----
    def find_all(text: str = None):
        key("ctrl-shift-f")
        if text:
            insert(text)
    def find_file(text: str = None):
        key("ctrl-shift-t")
        if text:
            insert(text)

    # ----- Comments -----
    def comment():           key("ctrl-k ctrl-c")
    def uncomment():         key("ctrl-k ctrl-u")

    # ----- Run -----
    def run_program():       key("ctrl-f5")
    def debug_program():     key("f5")
    def debug_breakpoint():  key("f9")
    def debug_continue():    key("f5")
    def debug_step_over():   key("f10")
    def debug_step_into():   key("f11")
    def debug_step_out():    key("shift-f11")
    def debug_restart():     key("ctrl-shift-f5")
    def debug_stop():        key("shift-f5")

    # ----- Misc -----
    def quick_fix():         key("ctrl-.")


@ctx.action_class("edit")
class EditActions:
    # ----- Line commands -----
    def line_swap_up():   key("alt-up")
    def line_swap_down(): key("alt-down")
    def line_clone():     key("ctrl-d")

    def jump_line(n: int):
        key("ctrl-g")
        insert(n)
        key("enter")

    # ----- Indent -----
    def indent_less():    key("shift-tab")

    # ----- Zoom -----
    def zoom_in():
        key("ctrl:down")
        actions.mouse_scroll(-1)
        key("ctrl:up")
    def zoom_out():
        key("ctrl:down")
        actions.mouse_scroll(1)
        key("ctrl:up")
    def zoom_reset():       skip()
