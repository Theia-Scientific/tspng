#!/usr/bin/env python3

import os
import pytest

from tspng.implantation import implant, implant_from_file
from tspng.extraction import extract


def test_implant():
    """
    Tests the dictionary keys from an example TSPNG file path.
    """

    implant("tests/assets/coco_data.json", "tests/assets/empty.png")
    test_data = extract("tests/assets/empty.ts.png")
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


def test_implant_from_file():
    """
    Tests the dictionary keys from an example TSPNG file path.
    """

    implant_from_file("tests/assets/coco_data.json", "tests/assets/empty.png")
    test_data = extract("tests/assets/empty.ts.png")
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
        implant_from_file("tests/assets", "tests/assets/empty.png")


def test_implant_from_file_fails_existence():
    with pytest.raises(Exception):
        implant_from_file("tests/assets/no_such_file.json", "tests/assets/empty.png")
