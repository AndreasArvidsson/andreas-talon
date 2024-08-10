from talon import Module, Context, actions

mod = Module()
ctx = Context()

mod.list("copilot_command", "Commands that can be used with copilot, e.g. /fix")
ctx.lists["user.copilot_command"] = {
    "test": "tests",
    "dock": "doc",
    "fix": "fix",
    "explain": "explain",
    "change": "",
}


@mod.action_class
class Actions:
    def copilot_inline_chat(command: str = "", text: str = ""):
        """Start copilot inline chat session"""
        actions.user.vscode(
            "editor.action.codeAction",
            {
                "kind": "refactor.rewrite",
            },
        )
        if command or text:
            actions.sleep("50ms")
            if command:
                command = f"/{command} "
            actions.insert(f"{command}{text}")
            actions.key("enter")

    def copilot_chat(text: str = ""):
        """Start copilot chat session"""
        actions.user.vscode("workbench.panel.chat.view.copilot.focus")
        if text:
            actions.sleep("50ms")
            actions.insert(text)
            actions.key("enter")
