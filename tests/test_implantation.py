#!/usr/bin/env python3

import pytest

from pathlib import Path
from tspng.implantation import implant, implant_into_file
from tspng.extraction import extract


def test_implant(coco_json_path, empty_png_path):
    """
    Tests the dictionary keys from an example TSPNG file path.
    """

    implant(coco_json_path, empty_png_path)
    ts_png = Path(empty_png_path).with_suffix(".ts.png")
    test_data = extract(ts_png)
    assert list(test_data.keys()) == [
        "info",
        "licenses",
        "images",
        "annotations",
        "models",
        "categories",
    ]


def test_implant_fails():
    with pytest.raises(TypeError):
        implant("Test for failure", "tests/assets/empty.png")


def test_implant_into_file(coco_json_path, empty_png_path):
    """
    Tests the dictionary keys from an example TSPNG file path.
    """

    implant_into_file(coco_json_path, empty_png_path)
    ts_png = Path(empty_png_path).with_suffix(".ts.png")
    test_data = extract(ts_png)
    assert list(test_data.keys()) == [
        "info",
        "licenses",
        "images",
        "annotations",
        "models",
        "categories",
    ]


def test_implant_from_file_fails_with_folder():
    with pytest.raises(Exception):
        implant_into_file("tests/assets", "tests/assets/empty.png")


def test_implant_from_file_fails_existence():
    with pytest.raises(Exception):
        implant_into_file("tests/assets/no_such_file.json", "tests/assets/empty.png")
