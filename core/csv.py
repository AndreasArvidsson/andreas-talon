from talon import Module, actions, resource
from typing import Callable, Tuple
from pathlib import Path
import csv

mod = Module()

RowType = list[str]
ListType = list[RowType]
DictType = dict[str, str]
TupleType = Tuple[ListType, RowType]


@mod.action_class
class Actions:
    def watch_csv_as_list(path: Path, callback: Callable[[ListType, RowType], None]):
        """Watch csv file for changes. Present content as list"""

        if not path.is_file():
            raise Exception(f"{path} is not a file")

        @resource.watch(path)
        def on_watch(f):
            callback(*read_csv_file(f))

    def watch_csv_as_dict(
        path: Path,
        callback: Callable[[dict], None],
        values_as_list: bool = False,
    ):
        """Watch csv file for changes. Present content as dict"""

        def on_watch(values: ListType, headers: RowType):
            if values_as_list:
                csv_dict = list_to_dict_of_lists(values)
            else:
                csv_dict = list_to_dict(path, values)
            callback(csv_dict)

        actions.user.watch_csv_as_list(path, on_watch)


def list_to_dict(path: Path, values: ListType) -> DictType:
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


def list_to_dict_of_lists(values: ListType) -> dict[str, RowType]:
    result = {}
    for row in values:
        result[row[0]] = row[1:]
    return result


def read_csv_file(file) -> TupleType:
    """Read csv file and return tuple with values and headers"""
    result = []

    # Use `skipinitialspace` to allow spaces before quote. `, "a,b"`
    csv_reader = csv.reader(file, skipinitialspace=True)
    for row in csv_reader:
        # Remove trailing whitespaces for each cell
        row = [x.rstrip() for x in row]
        # Exclude empty or comment rows
        if len(row) == 0 or (len(row) == 1 and row[0] == "") or row[0].startswith("#"):
            continue
        result.append(row)
    return parse_headers(result)


def parse_headers(csv_list: ListType) -> TupleType:
    """Separate csv list into values and headers"""
    if len(csv_list) > 1 and len(csv_list[1]) == 1 and csv_list[1][0] == "-":
        return csv_list[2:], csv_list[0]
    return csv_list, []
