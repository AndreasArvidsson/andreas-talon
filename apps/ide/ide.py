from talon import Module

mod = Module()
mod.tag("ide")


@mod.action_class
class Actions:
    # ----- Navigation -----
    def declaration_go():
        """Go to declaration"""
    def definition_go():
        """Go definition"""
    def definition_peek():
        """Peek definition"""
    def definition_split():
        """Open definition in split"""
    def references_go():
        """Go to references"""
    def references_peek():
        """Peek references"""

    # ----- Format -----
    def format_document():
        """Auto indent document"""
    def format_selection():
        """Auto indent selection"""

    # ----- Comments -----
    def comment():
        """Comment selected lines"""
    def uncomment():
        """Uncomment selected lines"""

    # ----- Run -----
    def run_program():
        """Run program"""
    def debug_program():
        """Debug program"""
    def debug_breakpoint():
        """Debug break point"""
    def debug_continue():
        """Debug continue"""
    def debug_step_over():
        """Debug step over"""
    def debug_step_into():
        """Debug step into"""
    def debug_step_out():
        """Debug step out"""
    def debug_restart():
        """Debug restart"""
    def debug_pause():
        """Debug pause"""
    def debug_stop():
        """Debug stop"""

    # ----- Misc -----
    def quick_fix():
        """Quick fix"""
