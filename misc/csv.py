from talon import Module, actions, fs
from typing import Callable
from pathlib import Path
import csv

mod = Module()

csv_directory_setting = mod.setting(
    "csv_directory", type=str, default="", desc="The directory to look for csv files"
)


@mod.action_class
class Actions:
    def watch_csv_as_list(path: str, callback: Callable[[list], None]):
        """Watch csv file for changes. Present content as list"""
        full_path = get_full_path(path)

        def on_watch(path: str, flags):
            if full_path.match(path):
                csv_list = read_csv_file(full_path)
                callback(csv_list)

        fs.watch(str(full_path.parent), on_watch)

        if full_path.is_file():
            csv_list = read_csv_file(full_path)
            callback(csv_list)

    def watch_csv_as_dict(path: str, callback: Callable[[dict], None]):
        """Watch csv file for changes. Present content as dict"""

        def on_watch(csv_list: list):
            csv_dict = list_to_dict(path, csv_list)
            callback(csv_dict)

        actions.user.watch_csv_as_list(path, on_watch)


def list_to_dict(path: str, csv_list: list) -> dict:
    result = {}
    # Exclude header row
    for row in csv_list[1:]:
        key = row[0].lower()
        if len(row) == 1:
            result[key] = row[0]
        elif len(row) == 2:
            result[key] = row[1]
        else:
            raise ValueError(
                f"Can't create dict from csv '{path}' with row length {len(row)}"
            )
    return result


def read_csv_file(path: Path) -> list:
    result = []
    with open(path, "r") as csv_file:
        csvReader = csv.reader(csv_file)
        for row in csvReader:
            # Exclude empty or comment rows
            if len(row) == 0 or row[0].lstrip().startswith("#"):
                continue
            result.append([x.strip() for x in row])
    return result


def get_full_path(path: str) -> Path:
    """Convert string file path to full absolute Path"""
    if not path.endswith(".csv"):
        path = f"{path}.csv"

    path = Path(path)

    if not path.is_absolute():
        directory = Path(csv_directory_setting.get())
        if not directory.is_absolute():
            directory = actions.path.talon_user() / directory
        path = directory / path

    return path.resolve()
