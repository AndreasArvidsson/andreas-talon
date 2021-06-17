from talon import Module, actions

mod = Module()
mod.tag("generic_language")

mod.list("code_member_op", desc="Operators to access members")
mod.list("code_function", desc="Names of functions")
mod.list("code_member", desc="Names of member")
mod.list("code_data_type", desc="Names of data types")
mod.list("code_access_modifier", desc="Names of access modifiers")
mod.list("code_statement", desc="Names of miscellaneous statements")


@mod.action_class
class tab_actions:
    # ----- Selection statements -----
    def code_if():
        """If statement"""
    def code_elif():
        """Else if statement"""
    def code_else():
        """Else statement"""
    def code_switch():
        """Switch statement"""
    def code_case():
        """case statement"""
    def code_default():
        """Switch default statement"""

    # ----- Iteration statements -----
    def code_for():
        """For loop statement"""
    def code_while():
        """while statement"""
    def code_do_while():
        """Do while loop statements"""
    def code_foreach():
        """Code foreach"""

    # ----- Miscellaneous statements -----
    def code_true():
        """Boolean true"""
    def code_false():
        """Boolean false"""
    def code_break():
        """break statement"""
    def code_continue():
        """continue statement"""
    def code_return():
        """return statement"""
    def code_print(text: str):
        """Print statement"""
    def code_comment():
        """Inline comment"""
    def code_block_comment():
        """Block comment"""

    # ----- Class statement -----
    def code_class(access_modifier: str or None, name: str):
        """Class statement"""

    # ----- Constructor statement -----
    def code_constructor(access_modifier: str or None):
        """Constructor statement"""

    # ----- Function statement -----
    def code_function(access_modifier: str or None, name: str):
        """Function statement"""

    # ----- Variable statement -----
    def code_variable(access_modifier: str or None, data_type: str or None, name: str, assign: str or None):
        """Variable statement"""

    # ----- Function call -----
    def code_call_function(name: str):
        """Function call"""

    # ----- Member access -----
    def code_member_access(operator: str, name: str):
        """Code member access"""

    # ----- Formatting getters -----
    def code_get_class_format() -> str:
        """Get variable format"""
    def code_get_function_format() -> str:
        """Get function format"""
    def code_get_variable_format() -> str:
        """Get variable format"""
