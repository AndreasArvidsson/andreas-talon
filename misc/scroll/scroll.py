from talon import Module

mod = Module()
mod.tag("scroll")

@mod.action_class
class Actions:
    def scrollUp():
        """Scroll up"""
    def scrollDown():
        """Scroll down"""
    def scrollLeft():
        """Scroll left"""
    def scrollRight():
        """Scroll right"""
    def scrollUpPage():
        """Scroll up page"""
    def scrollDownPage():
        """Scroll down page"""
    def scrollUpHalfPage():
        """Scroll up half page"""
    def scrollDownHalfPage():
        """Scroll down half page"""
