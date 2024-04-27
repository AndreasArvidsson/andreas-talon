from typing import Any
from uuid import uuid4

from talon import actions

from .types import Request
from .get_communication_dir_path import get_communication_dir_path
from .write_request import write_request
from .read_json_with_timeout import read_json_with_timeout
from .robust_unlink import robust_unlink


class RpcClient:
    def __init__(self, name: str, key: str):
        self.key = key
        self.dir_path = get_communication_dir_path(name)
        self.request_path = self.dir_path / "request.json"
        self.response_path = self.dir_path / "response.json"

    def send(
        self,
        data: Any,
        wait_for_finish: bool = False,
        return_command_output: bool = False,
    ):
        if not self.dir_path.exists():
            raise FileNotFoundError(
                f"RPC communication directory '{self.dir_path}' not found"
            )

        # Generate uuid that will be mirrored back to us by command server for
        # sanity checking
        uuid = str(uuid4())

        request = Request(
            wait_for_finish=wait_for_finish,
            return_command_output=return_command_output,
            data=data,
            uuid=uuid,
        )

        # First, write the request to the request file, which makes us the sole
        # owner because all other processes will try to open it with 'x'
        write_request(request, self.request_path)

        # We clear the response file if it does exist, though it shouldn't
        if self.response_path.exists():
            print("WARNING: Found old response file")
            robust_unlink(self.response_path)

        actions.key(self.key)

        try:
            decoded_contents = read_json_with_timeout(self.response_path)
        finally:
            # NB: We remove response file first because we want to do this while we
            # still own the request file
            robust_unlink(self.response_path)
            robust_unlink(self.request_path)

        if decoded_contents["uuid"] != uuid:
            raise Exception("uuids did not match")

        for warning in decoded_contents["warnings"]:
            print(f"WARNING: {warning}")

        if decoded_contents["error"] is not None:
            raise Exception(decoded_contents["error"])

        actions.sleep("25ms")

        if "returnValue" in decoded_contents:
            return decoded_contents["returnValue"]

        return None
