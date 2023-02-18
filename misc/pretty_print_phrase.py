from talon import Module

mod = Module()


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


@mod.action_class
class Actions:
    def pretty_print_phrase(phrase_str: str, sim: str, commands: list):
        """Pretty prints the command information to the terminal"""

        print(f"{bcolors.ENDC}=============================={bcolors.ENDC}")
        print(
            f"{bcolors.BOLD}Command:{bcolors.ENDC} {bcolors.GREEN}{bcolors.BOLD}{phrase_str}{bcolors.ENDC}"
        )

        # Render the individual commands nicely.
        if commands:
            for cmd in commands:
                rule = cmd["rule"] if "rule" in cmd else ""
                print(
                    " "
                    + " ".join(
                        [
                            f"#{cmd['num']}:",
                            f"{bcolors.BOLD}{cmd['phrase']}{bcolors.ENDC}:",
                            f"{cmd['path']} {bcolors.GREEN}{rule}{bcolors.ENDC}",
                        ]
                    ).strip()
                )
        else:
            print(
                f"{bcolors.BOLD}{bcolors.RED}Couldn't parse sim: {bcolors.ENDC}|{sim}|"
            )

        print(f"{bcolors.ENDC}=============================={bcolors.ENDC}")
