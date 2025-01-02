from talon import actions, app

rpc_key = "cmd-shift-f18" if app.platform == "mac" else "ctrl-shift-alt-o"
rpc_dir_name = "clippy-command-server"
rpc_command_id = "clippyCommand"


def rpc(command: dict):
    _rpc_command(command, wait_for_finish=True)


def rpc_get(command: dict):
    return _rpc_command(command, return_command_output=True)


def _rpc_command(
    command: dict,
    wait_for_finish: bool = False,
    return_command_output: bool = False,
):
    return actions.user.rpc_client_run_command(
        rpc_dir_name,
        lambda: actions.key(rpc_key),
        rpc_command_id,
        [command],
        wait_for_finish,
        return_command_output,
    )
