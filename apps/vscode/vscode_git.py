from typing import List, Optional
from talon import Context, Module, actions

mod = Module()

ctx = Context()
ctx.matches = r"""
app: vscode
not tag: terminal
"""


@ctx.action_class("user")
class Actions:
    def git_clone():
        actions.user.vscode("git.clone")

    def git_status():
        actions.user.vscode("workbench.scm.focus")

    def git_stage_all():
        actions.user.vscode("git.stageAll")

    def git_unstage_all():
        actions.user.vscode("git.unstageAll")

    def git_pull():
        actions.user.vscode("git.pull")

    def git_push():
        actions.user.vscode("git.push")

    def git_push_tags():
        actions.user.vscode("git.pushTags")

    def git_create_tag(tag: Optional[str] = None):
        command_with_text("git.createTag", tag)

    def git_show_tags():
        actions.user.vscode("gitlens.showTagsView")

    def git_stash():
        actions.user.vscode("git.stash")

    def git_stash_pop():
        actions.user.vscode("git.stashPop")

    def git_merge(branch: Optional[str] = None):
        command_with_text("git.merge", branch)

    def git_checkout(branch: Optional[str] = None, submit: bool = False):
        if branch in ["master", "main"]:
            actions.user.vscode("andreas.gitCheckoutDefaultBranch")
        else:
            command_with_text("git.checkout", branch, submit)

    def git_show_branches():
        actions.user.vscode("gitlens.showBranchesView")

    def git_create_branch(branch: Optional[str] = None):
        command_with_text("git.branch", branch)

    def git_delete_branch(branch: Optional[str] = None):
        command_with_text("git.deleteBranch", branch)

    def git_commit(message: Optional[str] = None):
        actions.user.vscode("git.commit")
        if message:
            actions.sleep("200ms")
            actions.insert(message)

    def git_commit_amend(message: Optional[str] = None):
        actions.user.vscode("git.commitAmend")
        if message:
            actions.sleep("200ms")
            actions.insert(message)

    def git_commit_empty():
        actions.user.vscode("git.commitEmpty")

    def git_diff():
        actions.user.vscode("git.openChange")

    def git_stash_show():
        actions.user.vscode("gitlens.showQuickStashList")

    def git_stash_list():
        actions.user.vscode("gitlens.showQuickStashList")

    def git_log():
        actions.user.vscode("gitlens.showCommitsView")

    def git_remote():
        actions.user.vscode("gitlens.showRemotesView")

    def git_cherry_pick():
        actions.user.vscode("git.cherryPick")


@mod.action_class
class Actions:
    def git_open_remote_file_url(use_selection: bool, use_branch: bool):
        """Open remote git file in browser"""
        url = actions.user.vscode_get(
            "andreas.getGitFileURL",
            {"useSelection": use_selection, "useBranch": use_branch},
        )
        if url:
            actions.user.browser_open(url)

    def git_copy_remote_file_url(use_selection: bool, use_branch: bool):
        """Copy remote git file URL to clipboard"""
        url = actions.user.vscode_get(
            "andreas.getGitFileURL",
            {"useSelection": use_selection, "useBranch": use_branch},
        )
        if url:
            actions.clip.set_text(url)

    def git_open_url(command: str):
        """Open remote repository in browser"""
        url = actions.user.vscode_get(f"andreas.getGit{command}URL")
        if url:
            actions.user.browser_open(url)

    def git_copy_markdown_remote_file_url(targets: List):
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

        url = actions.user.vscode_get(
            "andreas.getGitFileURL",
            {"useSelection": use_selection, "useBranch": False},
        )
        if url and text:
            actions.clip.set_text(f"[`{text}`]({url})")


def command_with_text(command: str, text: Optional[str] = None, submit: bool = False):
    actions.user.vscode(command)
    if text:
        actions.sleep("50ms")
        actions.insert(text)
        actions.sleep("50ms")
    if submit:
        actions.key("enter")
