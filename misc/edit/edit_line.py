from talon import Context, Module, actions

key = actions.key
edit = actions.edit
user = actions.user

ctx = Context()
mod = Module()


@ctx.action_class("edit")
class EditActions:
    def line_start():
        key("home")

    def line_end():
        key("end")

    def select_line(n: int = None):
        if n:
            edit.jump_line(n)
        key("end shift-home")

    def select_lines(a: int, b: int):
        number_of_lines = abs(a - b)
        if number_of_lines < 1 or number_of_lines > 500:
            return
        edit.jump_line(a)
        if a < b:
            for _ in range(number_of_lines):
                edit.extend_line_down()
            edit.extend_line_end()
        else:
            edit.line_end()
            for _ in range(number_of_lines):
                edit.extend_line_up()
            edit.extend_line_start()

    def extend_line_up():
        key("shift-up")

    def extend_line_down():
        key("shift-down")

    def extend_line_start():
        key("shift-home")

    def extend_line_end():
        key("shift-end")

    def line_insert_up():
        key("home enter up")

    def line_insert_down():
        key("end enter")

    def line_clone():
        user.copy_line()
        edit.line_insert_down()
        edit.paste()

    def line_swap_up():
        user.cut_line()
        edit.line_start()
        edit.paste()
        key("enter up")

    def line_swap_down():
        user.cut_line()
        key("down end enter")
        edit.paste()

    def delete_line():
        user.clear_line()
        key("home delete")


@mod.action_class
class Actions:
    def line_middle(n: int = None):
        """Move cursor to middle of line <n> or current"""
        if n:
            edit.jump_line(n)
        edit.select_line()
        text = edit.selected_text().strip()
        edit.right()
        for _ in range(round(len(text) / 2)):
            edit.left()

    def cut_line(n: int = None):
        """Cut line <n> or current"""
        if n:
            edit.jump_line(n)
        edit.select_line()
        edit.cut()
        edit.delete()

    def copy_line(n: int = None):
        """Copy line <n> or current"""
        if n:
            edit.jump_line(n)
        edit.select_line()
        edit.copy()

    def clone_line(n: int = None):
        """Clone line <n> or current"""
        if n:
            edit.jump_line(n)
        edit.line_clone()

    def line_insert_down_twice():
        """Insert two lines below cursor"""
        edit.line_insert_down()
        edit.line_insert_down()

    def clear_line(n: int = None):
        """Clear line <n> or current"""
        if n:
            edit.jump_line(n)
        key("end shift-home space backspace")

    def delete_line(n: int = None):
        """Delete line <n> or current"""
        if n:
            edit.jump_line(n)
        edit.delete_line()

    # ----- Start / End -----
    def select_line_start():
        """Select start of line"""
        if edit.selected_text():
            edit.left()
        edit.extend_line_start()

    def select_line_end():
        """Select end of line"""
        if edit.selected_text():
            edit.right()
        edit.extend_line_end()

    def cut_line_start():
        """Cut start of line"""
        edit.extend_line_start()
        edit.cut()

    def cut_line_end():
        """Cut end of line"""
        edit.extend_line_end()
        edit.cut()

    def copy_line_start():
        """Copy start of line"""
        edit.extend_line_start()
        edit.copy()
        edit.right()

    def copy_line_end():
        """Copy end of line"""
        edit.extend_line_end()
        edit.copy()
        edit.left()

    def delete_line_start():
        """Delete start of current line"""
        edit.extend_line_start()
        edit.delete()

    def delete_line_end():
        """Delete end of current line"""
        edit.extend_line_end()
        edit.delete()
