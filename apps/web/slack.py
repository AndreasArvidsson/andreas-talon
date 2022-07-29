from talon import Context, Module, actions
from talon.clip import MimeData
import json
import re

ctx = Context()
mod = Module()

mod.apps.slack = """
tag: browser
and title: /Slack/
"""

ctx.matches = """
app: slack
"""


@ctx.action_class("edit")
class EditActions:
    def line_insert_up():
        actions.key("home ctrl-enter up")

    def line_insert_down():
        actions.key("end ctrl-enter")


@mod.action_class
class UserActions:
    def slack_open_search_result(search: str):
        """Opens the given search result on slack"""
        actions.key("ctrl-k")
        actions.insert(search)
        actions.sleep("400ms")
        actions.key("enter")

    def slack_mime_to_markdown(mime: MimeData) -> str:
        """Convert mine type to markdown for slack"""
        slack_format = 'application/x-qt-windows-mime;value="slack/texty"'
        if slack_format in mime.formats:
            try:
                # For some reason the last character is not compatible with json encoding
                data_str = mime[slack_format].decode("utf-16")[:-1]
                # print(data_str)
                data = json.loads(data_str)
                return json_to_markdown(data)
            except Exception as e:
                print(e)
        return ""


def json_to_markdown(data: dict) -> str:
    ops = data["ops"]
    result = ""
    current_block = ""

    for i, op in enumerate(ops):
        attributes = get_attributes(ops, i)
        attributes_next = get_attributes(ops, i + 1)
        insert = op["insert"]

        if is_block_element(attributes):
            # Trailing spaces are required for new lines in block quotes
            if attributes.get("blockquote"):
                insert = insert.replace("\n", "  \n")
            elif attributes.get("list"):
                insert, current_block = format_list_block(
                    insert, attributes, current_block
                )
            result += insert
            continue

        lines = re.split("(\n)", insert)
        lines = [l for l in lines if l != ""]
        # print(lines)

        for j, line in enumerate(lines):
            trailing_nl = line.endswith("\n")
            line = apply_attributes(line, attributes)
            if j == len(lines) - 1:
                line, current_block = apply_block_attributes(
                    line, attributes_next, current_block
                )
            if trailing_nl:
                line = line.replace("\n", "  \n")
            result += line
            # print(f"> '{[line]}'")

    return result


def apply_block_attributes(line: str, attributes: dict, current_block: str):
    if attributes.get("code-block"):
        if current_block != "code-block":
            current_block = "code-block"
            line = f"```\n{line}"
    elif attributes.get("blockquote"):
        line = f"> {line}"
        if current_block != "blockquote":
            current_block = "blockquote"
            line = f"\n{line}"
    elif attributes.get("list"):
        if line == "\n" and current_block != attributes.get("list"):
            line = line + line + format_list_line("", attributes["list"])
        else:
            line = format_list_line(line, attributes["list"])
        current_block = attributes["list"]
    else:
        if current_block == "code-block":
            line = f"```\n{line}"
        elif current_block == "blockquote":
            line = f"\n{line}"
        current_block = ""
    return line, current_block


def format_list_block(insert: str, attributes: dict, current_block: str) -> str:
    lines = insert.splitlines(True)
    type = attributes["list"]

    for i in range(len(lines)):
        # The first line is already formatted in the previous lookahead
        if i > 0 or current_block != type:
            lines[i] = format_list_line(lines[i], type)
            if i == 0:
                lines[i] = f"\n{lines[i]}"
    return "".join(lines), type


def format_list_line(line: str, type: str) -> str:
    if type == "bullet":
        return f"- {line}"
    elif type == "ordered":
        return f"1. {line}"


def apply_attributes(line: str, attributes: dict) -> str:
    if attributes.get("strike"):
        line = f"~~{line}~~"
    if attributes.get("italic"):
        line = f"*{line}*"
    if attributes.get("bold"):
        line = f"**{line}**"
    if attributes.get("code"):
        line = f"`{line}`"
    if attributes.get("link"):
        line = f"[{line}]({attributes['link']})"
    return line


def is_block_element(attributes: dict) -> bool:
    block_elements = ["code-block", "blockquote", "list"]
    for element in block_elements:
        if element in attributes:
            return True
    return False


def get_attributes(ops: dict, index: int) -> dict:
    try:
        return ops[index]["attributes"]
    except:
        return {}
