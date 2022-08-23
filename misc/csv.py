from talon import Module, actions, fs
from typing import Callable, Tuple
from pathlib import Path
import csv

mod = Module()

RowType = list[str]
ListType = list[RowType]
DictType = dict[str, str]
TupleType = Tuple[ListType, RowType]

csv_directory_setting = mod.setting(
    "csv_directory", type=str, default="", desc="The directory to look for csv files"
)


@mod.action_class
class Actions:
    def watch_csv_as_list(path: str, callback: Callable[[ListType, RowType], None]):
        """Watch csv file for changes. Present content as list"""
        full_path = get_full_path(path)

        def on_watch(path: str, flags):
            if full_path.match(path):
                callback(*read_csv_file(full_path))

        fs.watch(str(full_path.parent), on_watch)

        if full_path.is_file():
            callback(*read_csv_file(full_path))

    def watch_csv_as_dict(
        path: str,
        callback: Callable[[dict], None],
        values_as_list: bool = False,
    ):
        """Watch csv file for changes. Present content as dict"""

        def on_watch(values: ListType, headers: RowType):
            if values_as_list:
                csv_dict = list_to_dict_of_lists(path, values)
            else:
                csv_dict = list_to_dict(path, values)
            callback(csv_dict)

        actions.user.watch_csv_as_list(path, on_watch)


def list_to_dict(path: str, values: ListType) -> DictType:
    result = {}
    for row in values:
        if len(row) == 1:
            result[row[0]] = row[0]
        elif len(row) == 2:
            result[row[0]] = row[1]
        else:
            raise ValueError(
                f"Can't create dict from csv '{path}' with row length {len(row)}"
            )
    return result


def list_to_dict_of_lists(path: str, values: ListType) -> dict[str, RowType]:
    result = {}
    for row in values:
        result[row[0]] = row[1:]
    return result


def read_csv_file(path: Path) -> TupleType:
    """Read csv file and return tuple with values and headers"""
    result = []
    with open(path, "r") as csv_file:
        # Use `skipinitialspace` to allow spaces before quote. `, "a,b"`
        csv_reader = csv.reader(csv_file, skipinitialspace=True)
        for row in csv_reader:
            # Remove trailing whitespaces for each cell
            row = [x.rstrip() for x in row]
            # Exclude empty or comment rows
            if (
                len(row) == 0
                or (len(row) == 1 and row[0] == "")
                or row[0].startswith("#")
            ):
                continue
            result.append(row)
    return parse_headers(result)


def parse_headers(csv_list: ListType) -> TupleType:
    """Separate csv list into values and headers"""
    if len(csv_list) > 1 and len(csv_list[1]) == 1 and csv_list[1][0] == "-":
        return csv_list[2:], csv_list[0]
    return csv_list, []


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
