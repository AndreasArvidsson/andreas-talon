from dataclasses import dataclass
from typing import Any


@dataclass
class Request:
    uuid: str
    data: Any
    wait_for_finish: bool
    return_command_output: bool

    def to_dict(self):
        return {
            "uuid": self.uuid,
            "data": self.data,
            "waitForFinish": self.wait_for_finish,
            "returnCommandOutput": self.return_command_output,
        }
