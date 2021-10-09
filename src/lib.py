from functools import reduce
from pathlib import Path
import operator
import json
import csv


def get_by_path(root, items):
    """Access a nested object in root by item sequence."""
    return reduce(operator.getitem, items, root)


def set_by_path(root, items, value):
    """Set a value in a nested object in root by item sequence."""
    get_by_path(root, items[:-1])[items[-1]] = value


def read_json(path: Path) -> dict:
    with open(str(path), "r", encoding="utf-8") as f:
        j = json.load(f)
    return j


def write_csv(header: list, data: list, path: Path) -> None:
    with open(str(path), "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(data)
