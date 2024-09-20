from talon import Module
from typing import Iterable, Tuple
import csv

mod = Module()

RowType = list[str]
ListType = list[RowType]
TupleType = Tuple[ListType, RowType]


@mod.action_class
class Actions:
    def read_csv_as_list(file: Iterable[str]) -> ListType:
        """Read csv file. Present content as list"""
        values, headers = read_csv_file(file)
        return values

    def read_csv_as_dict(file: Iterable[str]) -> dict[str, str]:
        """Read csv file. Present content as dict"""
        values, headers = read_csv_file(file)

        result = {}
        for row in values:
            if len(row) == 1:
                result[row[0]] = row[0]
            elif len(row) == 2:
                result[row[0]] = row[1]
            else:
                raise ValueError(
                    f"Can't create dict from csv with row length {len(row)}"
                )
        return result

    def read_csv_as_dict_of_lists(file: Iterable[str]) -> dict[str, RowType]:
        """Read csv file. Present content as dict of lists"""
        values, headers = read_csv_file(file)
        result = {}
        for row in values:
            result[row[0]] = row[1:]
        return result


def read_csv_file(file: Iterable[str]) -> TupleType:
    """Read csv file and return tuple with values and headers"""
    result: ListType = []

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
