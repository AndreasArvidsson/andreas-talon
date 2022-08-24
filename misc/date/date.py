from talon import Module
from datetime import date, timedelta

mod = Module()
format = "%Y-%m-%d"


@mod.action_class
class Actions:
    def date_today() -> str:
        """Return string with todays date"""
        return date.today().strftime(format)

    def date_yesterday() -> str:
        """Return string with yesterdays date"""
        return (date.today() - timedelta(days=1)).strftime(format)

    def date_tomorrow() -> str:
        """Return string with tomorrow date"""
        return (date.today() + timedelta(days=1)).strftime(format)
