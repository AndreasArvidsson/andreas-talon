from typing import Optional
from talon import Context, Module, actions

mod = Module()

ctx = Context()
ctx.matches = r"""
app: vscode
not tag: terminal
"""


@ctx.action_class("user")
class UserActions:
    def git_clone():
        actions.user.run_rpc_command("git.clone")

    def git_status():
        actions.user.run_rpc_command("workbench.scm.focus")

    def git_stage_all():
        actions.user.run_rpc_command("git.stageAll")

    def git_unstage_all():
        actions.user.run_rpc_command("git.unstageAll")

    def git_pull():
        actions.user.run_rpc_command("git.pull")

    def git_push():
        actions.user.run_rpc_command("git.push")

    def git_push_tags():
        actions.user.run_rpc_command("git.pushTags")

    def git_create_tag(tag: Optional[str] = None):
        command_with_text("git.createTag", tag)

    def git_show_tags():
        actions.user.run_rpc_command("gitlens.showTagsView")

    def git_stash():
        actions.user.run_rpc_command("git.stash")

    def git_stash_pop():
        actions.user.run_rpc_command("git.stashPop")

    def git_stash_drop():
        actions.user.run_rpc_command("git.stashDrop")

    def git_merge(branch: Optional[str] = None):
        if branch:
            branches = get_branch_names_with_fallback(branch)
            if len(branches) > 1:
                first_branch = get_first_available_branch(branches)
                if first_branch:
                    branch = first_branch
        command_with_text("git.merge", branch)

    def git_checkout(branch: Optional[str] = None, submit: bool = False):
        if branch:
            branches = get_branch_names_with_fallback(branch)
            try:
                actions.user.run_rpc_command_and_wait("andreas.gitCheckout", *branches)
            except Exception:
                command_with_text("git.checkout", branch)
        else:
            command_with_text("git.checkout")

    def git_show_branches():
        actions.user.run_rpc_command("gitlens.showBranchesView")

    def git_create_branch(branch: Optional[str] = None):
        command_with_text("git.branch", branch)

    def git_delete_branch(branch: Optional[str] = None):
        command_with_text("git.deleteBranch", branch)

    def git_commit(message: Optional[str] = None):
        actions.user.run_rpc_command("git.commit")
        if message:
            actions.sleep("200ms")
            actions.insert(message)

    def git_commit_amend(message: Optional[str] = None):
        actions.user.run_rpc_command("git.commitAmend")
        if message:
            actions.sleep("200ms")
            actions.insert(message)

    def git_commit_empty():
        actions.user.run_rpc_command("git.commitEmpty")

    def git_diff():
        actions.user.run_rpc_command("git.openChange")

    def git_stash_show():
        actions.user.run_rpc_command("gitlens.showQuickStashList")

    def git_stash_list():
        actions.user.run_rpc_command("gitlens.showQuickStashList")

    def git_log():
        actions.user.run_rpc_command("gitlens.showCommitsView")

    def git_remote():
        actions.user.run_rpc_command("gitlens.showRemotesView")

    def git_cherry_pick():
        actions.user.run_rpc_command("git.cherryPick")


@mod.action_class
class Actions:
    def git_open_remote_file_url(use_selection: bool, use_branch: bool):
        """Open remote git file in browser"""
        url = actions.user.run_rpc_command_get(
            "andreas.getGitFileURL",
            {"useSelection": use_selection, "useBranch": use_branch},
        )
        if url:
            actions.user.browser_open(url)

    def git_copy_remote_file_url(use_selection: bool, use_branch: bool):
        """Copy remote git file URL to clipboard"""
        url = actions.user.run_rpc_command_get(
            "andreas.getGitFileURL",
            {"useSelection": use_selection, "useBranch": use_branch},
        )
        if url:
            actions.clip.set_text(url)

    def git_open_url(command: str):
        """Open remote repository in browser"""
        url = actions.user.run_rpc_command_get(f"andreas.getGit{command}URL")
        if url:
            actions.user.browser_open(url)

    def git_copy_markdown_remote_file_url(targets: list):
        """Copy remote git file URL to clipboard as markdown link"""
        use_selection = False
        text = ""

        # The second target is optional and is used for getting the text
        if len(targets) == 2:
            text = "".join(actions.user.cursorless_get_text_list(targets[1]))
            use_selection = True

        # The first target is the source of the git url
        actions.user.cursorless_command("setSelection", targets[0])

        # If the second target is omitted used the selected text
        if len(targets) == 1:
            text = actions.edit.selected_text()

        url = actions.user.run_rpc_command_get(
            "andreas.getGitFileURL",
            {"useSelection": use_selection, "useBranch": False},
        )
        if url and text:
            actions.clip.set_text(f"[`{text}`]({url})")


def command_with_text(command: str, text: Optional[str] = None):
    actions.user.run_rpc_command(command)
    if text:
        actions.sleep("50ms")
        actions.insert(text)


def get_first_available_branch(branches: list[str]) -> str | None:
    return actions.user.run_rpc_command_get(
        "andreas.gitGetFirstAvailableBranch", branches
    )


def get_branch_names_with_fallback(branch: str) -> list[str]:
    if branch == "main":
        return ["main", "master"]
    elif branch == "master":
        return ["master", "main"]
    else:
        return [branch]
