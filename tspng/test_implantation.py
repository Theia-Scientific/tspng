#!/usr/bin/env python3

import os
import pytest

from pathlib import Path
from tspng.implantation import implant, implant_into_file
from tspng.extraction import extract


def test_implant():
    """
    Tests the dictionary keys from an example TSPNG file path.
    """

    implant("tests/assets/coco_data.json", "tests/assets/empty.png")
    test_data = extract(Path("tests/assets/empty.ts.png"))
    assert list(test_data.keys()) == [
        "info",
        "licenses",
        "images",
        "annotations",
        "models",
        "categories",
    ]
    os.remove("tests/assets/empty.ts.png")


def test_implant_fails():
    with pytest.raises(TypeError):
        implant("Test for failure", "tests/assets/empty.png")


def test_implant_into_file():
    """
    Tests the dictionary keys from an example TSPNG file path.
    """

    implant_into_file("tests/assets/coco_data.json", "tests/assets/empty.png")
    test_data = extract(Path("tests/assets/empty.ts.png"))
    assert list(test_data.keys()) == [
        "info",
        "licenses",
        "images",
        "annotations",
        "models",
        "categories",
    ]
    os.remove("tests/assets/empty.ts.png")


def test_implant_from_file_fails_with_folder():
    with pytest.raises(Exception):
        implant_into_file("tests/assets", "tests/assets/empty.png")


def test_implant_from_file_fails_existence():
    with pytest.raises(Exception):
        implant_from_file("tests/assets/no_such_file.json", "tests/assets/empty.png")
