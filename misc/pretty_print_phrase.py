from talon import Module

mod = Module()

settings_log = mod.setting(
    "pretty_print_phrase",
    type=bool,
    default=False,
    desc="If true phrase will be pretty printed to the log",
)


@mod.action_class
class Actions:
    def pretty_print_phrase(phrase_str: str, commands: list):
        """Pretty prints the command information to the terminal"""
        if not settings_log.get():
            return

        print(f"{bcolors.ENDC}=============================={bcolors.ENDC}")
        print(
            f"{bcolors.BOLD}Command:{bcolors.ENDC} {bcolors.GREEN}{bcolors.BOLD}{phrase_str}{bcolors.ENDC}"
        )

        # Render the individual commands nicely.
        for cmd in commands:
            print(
                " ".join(
                    [
                        f"#{cmd['num']}:",
                        f"{bcolors.BOLD}{cmd['phrase']}{bcolors.ENDC}:",
                        f"file:{cmd['path']} {bcolors.GREEN}{cmd['rule']}{bcolors.ENDC}",
                    ]
                ).strip()
            )
            for action in cmd["actions"]:
                " ".join(
                    [
                        f"  {bcolors.BOLD}{action['name']}{bcolors.ENDC}:"
                        f"{action['desc']}"
                    ]
                )
                print(
                    f"  {bcolors.BOLD}{action['name']}{bcolors.ENDC}: {action['desc']}"
                )

        print(f"{bcolors.ENDC}=============================={bcolors.ENDC}")


class bcolors:
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKCYAN = "\033[96m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"
    RED = "\033[31m"
    GREEN = "\033[92m"
