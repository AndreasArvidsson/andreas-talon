from talon import Module, Context, actions

mod = Module()
ctx = Context()
mod.tag("git")

mod.list("git_branch", "List of common git branches")
ctx.lists["user.git_branch"] = {
    "master",
    "main",
    "develop",
}


@mod.action_class
class Action:
    def git_numstat(since: str or None):
        """Show git statistics"""
        args = "--author='Andreas Arvidsson'"
        if since:
            args = f"{args} --since '{since}'"
        awk = "awk 'NF==3 {plus+=$1; minus+=$2} END {printf(\"+%d, -%d\\n\", plus, minus)}'"
        actions.insert(f"git log --numstat {args} | {awk}\n")
