from talon import Module

mod = Module()
mod.tag("operators")

@mod.action_class
class Actions:
    # ----- Assignment operator -----
    def op_assign():
        """Assignment operator"""

    # ----- Math operators -----
    def op_sub():
        """Subtraction operator"""
    def op_sub_assign():
        """Subtraction assign operator"""
    def op_add():
        """Addition operator"""
    def op_add_assign():
        """Addition assign operator"""
    def op_mult():
        """Multiplication operator"""
    def op_mult_assign():
        """Multiply assign operator"""
    def op_div():
        """Division operator"""
    def op_div_assign():
        """Division assign operator"""
    def op_mod():
        """Module operator"""
    def op_mod_assign():
        """Module assign operator"""
    def op_exp():
        """Exponent operator"""

    # ----- Comparison operators -----
    def op_equal():
        """Boolean equal operator"""
    def op_not_equal():
        """Boolean not equal operator"""
    def op_less():
        """Boolean is less operator"""
    def op_greater():
        """Boolean is greater operator"""
    def op_less_or_eq():
        """Boolean is less or equal operator"""
    def op_greater_or_eq():
        """Boolean is greater or equal operator"""
    def op_not():
        """Boolean not operator"""
    def op_equal_null():
        """Boolean equal null operator"""
    def op_not_equal_null():
        """Boolean not equal null operator"""

    # ----- Logical operators -----
    def op_and():
        """Boolean and operator"""
    def op_or():
        """Boolean or operator"""
