from talon import Module
from datetime import date, timedelta

mod = Module()
date_format = "%Y-%m-%d"


# five o'clock         05:00
# five hundred hours   05:00
# five twenty five     05:25
# five oh five         05:05
@mod.capture(
    rule="<number_small> (<number_small> | oh {user.digit} | o'clock | hundred hours)"
)
def time(m) -> str:
    """24 hour time"""
    hours = str(m.number_small)
    try:
        minutes = str(m.number_small_2)
    except AttributeError:
        try:
            minutes = str(m.digit)
        except AttributeError:
            minutes = ""
    return f"{hours.rjust(2,'0')}:{minutes.rjust(2,'0')}"


@mod.capture(rule="time <user.time>")
def time_prose(m) -> str:
    """24 hour time with prose prefix"""
    return m.time


@mod.action_class
class Actions:
    def date_today() -> str:
        """Return date string for today"""
        return date.today().strftime(date_format)

    def date_delta_days(days: int) -> str:
        """Return date string for today + <delta> days"""
        return (date.today() + timedelta(days=days)).strftime(date_format)
