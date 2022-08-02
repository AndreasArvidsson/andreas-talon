import re
from talon import Module, Context, actions

ctx = Context()
mod = Module()

mod.list("navigation_action", desc="Action to perform")
ctx.lists["self.navigation_action"] = {"go", "select"}

mod.list("navigation_direction", desc="Direction to perform the action")
ctx.lists["self.navigation_direction"] = {"up", "down", "left", "right"}


@mod.action_class
class Actions:
    def navigation(action: str, direction: str, target: str):
        """Navigation"""
        if direction == "up":
            text = get_text_up()
            before_or_after = "after"
        elif direction == "down":
            text = get_text_down()
            before_or_after = "before"
        elif direction == "left":
            text = get_text_left()
            before_or_after = "after"
        elif direction == "right":
            text = get_text_right()
            before_or_after = "before"

        target = re.escape(target)
        num_lines = 0
        length = 0

        if direction == "up" or direction == "down":
            lines = text.split("\n")
            if direction == "up":
                for line in reversed(lines):
                    length = len(line)
                    m = search_line(direction, target, line, length)
                    if m:
                        break
                    num_lines += 1
            else:
                for line in lines:
                    length = len(line)
                    m = search_line(direction, target, line, length)
                    if m:
                        break
                    num_lines += 1
        else:
            length = len(text)
            m = search_line(direction, target, text, length)

        if not m:
            return

        if action == "go":
            handle_go(direction, before_or_after, num_lines, m.start(), m.end(), length)
        elif action == "select":
            handle_select(
                direction, before_or_after, num_lines, m.start(), m.end(), length
            )


def search_line(direction: str, target: str, text: str, length: int):
    matches = list(re.finditer(target, text, re.IGNORECASE))
    if len(matches) == 0:
        return None
    if direction == "right" or direction == "down":
        m = matches[0]
        if m.start() == 0 and len(matches) > 1:
            m = matches[1]
    else:
        m = matches[len(matches) - 1]
        if m.end() == length and len(matches) > 1:
            m = matches[len(matches) - 2]
    return m


def handle_go(direction, before_or_after, num_lines, start, end, length):
    if num_lines:
        go_lines(direction, num_lines)
    if direction == "up" or direction == "down":
        actions.edit.line_end()
    if direction == "right":
        if before_or_after == "before":
            go_right(start)
        else:
            go_right(end)
    else:
        if before_or_after == "before":
            go_left(length - start)
        else:
            go_left(length - end)


def handle_select(direction, before_or_after, num_lines, start, end, length):
    if num_lines:
        select_lines(direction, num_lines)
    if direction == "up" or direction == "down":
        actions.edit.extend_line_end()
    if direction == "right":
        if before_or_after == "before":
            extend_right(start)
        else:
            extend_right(end)
    else:
        if before_or_after == "before":
            extend_left(length - start)
        else:
            extend_left(length - end)


def get_text_up():
    actions.edit.up()
    actions.edit.line_end()
    actions.edit.extend_file_start()
    text = actions.edit.selected_text()
    actions.edit.right()
    return text


def get_text_down():
    actions.edit.down()
    actions.edit.line_start()
    actions.edit.extend_file_end()
    text = actions.edit.selected_text()
    actions.edit.left()
    return text


def get_text_left():
    actions.edit.extend_line_start()
    text = actions.edit.selected_text()
    actions.edit.right()
    return text


def get_text_right():
    actions.edit.extend_line_end()
    text = actions.edit.selected_text()
    actions.edit.left()
    return text


def go_lines(direction: str, count: int):
    if direction == "up":
        for _ in range(count):
            actions.edit.up()
    else:
        for _ in range(count):
            actions.edit.down()


def select_lines(direction: str, count: int):
    if direction == "up":
        for _ in range(count):
            actions.edit.extend_up()
    else:
        for _ in range(count):
            actions.edit.extend_down()


def go_left(i):
    for j in range(0, i):
        actions.edit.left()


def go_right(i):
    for j in range(0, i):
        actions.edit.right()


def extend_left(i):
    for j in range(0, i):
        actions.edit.extend_left()


def extend_right(i):
    for j in range(0, i):
        actions.edit.extend_right()
