from talon import Module, actions

mod = Module()
mod.tag("git")

@mod.action_class
class Action:
    def git_numstat(since: str or None):
        """Show git statistics"""
        args = "--author='Andreas Arvidsson'"
        if since:
            args = f"{args} --since '{since}'"
        awk = "awk 'NF==3 {plus+=$1; minus+=$2} END {printf(\"+%d, -%d\\n\", plus, minus)}'"
        actions.insert(f"git log --numstat {args} | {awk}\n")
