#!/usr/bin/env python3

import pytest

from io import BytesIO
from pathlib import Path
from tspng.extraction import (
    extract,
    extract_from_bytes,
    extract_from_file,
    extract_from_files,
    extract_from_folder,
    extract_from_url,
)


def test_extract():
    """
    Tests the dictionary keys from an example TSPNG file path.
    """
    # test bytes
    with open("tests/assets/example_file_1.ts.png", "rb") as fh:
        buf = BytesIO(fh.read())
        test_data = extract_from_bytes(buf)
        assert list(test_data.keys()) == [
            "info",
            "licenses",
            "images",
            "annotations",
            "models",
            "categories",
        ]
    # test file
    test_data = extract(Path("tests/assets/example_file_1.ts.png"))
    assert list(test_data.keys()) == [
        "info",
        "licenses",
        "images",
        "annotations",
        "models",
        "categories",
    ]
    # test list of files
    test_data = extract(
        [
            Path("tests/assets/example_file_1.ts.png"),
            Path("tests/assets/example_file_2.ts.png"),
        ]
    )
    assert list(test_data.keys()) == [
        Path("tests/assets/example_file_1.ts.png"),
        Path("tests/assets/example_file_2.ts.png"),
    ]
    # test folder
    test_data = extract(Path("tests/assets"))
    assert "tests/assets/example_file_1.ts.png" in sorted(list(test_data.keys()))
    assert "tests/assets/example_file_2.ts.png" in sorted(list(test_data.keys()))
    # test url
    test_data = extract(
        "https://bounding-box-instructions.s3.amazonaws.com/example_file_1.ts.png"
    )
    assert list(test_data.keys()) == [
        "info",
        "licenses",
        "images",
        "annotations",
        "models",
        "categories",
    ]


def test_extract_fails():
    with pytest.raises(TypeError):
        extract("Test for failure")


def test_extract_from_bytes():
    """
    Tests the dictionary keys from an example TS byte stream.
    """
    with open("tests/assets/example_file_1.ts.png", "rb") as fh:
        buf = BytesIO(fh.read())
        test_data = extract_from_bytes(buf)
        assert list(test_data.keys()) == [
            "info",
            "licenses",
            "images",
            "annotations",
            "models",
            "categories",
        ]


def test_extract_from_bytes_fails():
    with pytest.raises(TypeError):
        extract_from_bytes("tests/assets/example_file_1.ts.png")


def test_extract_from_file():
    """
    Tests the dictionary keys from an example TSPNG file path.
    """
    test_data = extract_from_file(Path("tests/assets/example_file_1.ts.png"))
    assert list(test_data.keys()) == [
        "info",
        "licenses",
        "images",
        "annotations",
        "models",
        "categories",
    ]


def test_extract_from_file_fails():
    # test folder instead of file
    with pytest.raises(Exception):
        extract_from_file(Path("Random/path.png"))
    # test file does not exist
    with pytest.raises(Exception):
        extract_from_file(Path("tests/assets"))


def test_extract_from_files():
    """
    Tests the dictionary keys from a list of example TSPNG file paths.
    """
    test_data = extract_from_files(
        [
            Path("tests/assets/example_file_1.ts.png"),
            Path("tests/assets/example_file_2.ts.png"),
        ]
    )
    assert sorted(list(test_data.keys())) == [
        Path("tests/assets/example_file_1.ts.png"),
        Path("tests/assets/example_file_2.ts.png"),
    ]


def test_extract_from_folder():
    """
    Tests the dictionary keys from a list of example TSPNG file paths.
    """
    test_data = extract_from_folder(Path("tests/assets"))
    assert "tests/assets/example_file_1.ts.png" in sorted(list(test_data.keys()))
    assert "tests/assets/example_file_2.ts.png" in sorted(list(test_data.keys()))


def test_extract_from_folder_fails():
    # test if directory
    with pytest.raises(Exception):
        extract_from_folder(Path("tests/assets/example_file_1.ts.png"))
    # test if PNG files in directory
    with pytest.raises(Exception):
        extract_from_folder(Path("tests"))


def test_extract_from_url():
    """
    Tests the dictionary keys from an example TSPNG url.
    """
    test_data = extract_from_url(
        "https://bounding-box-instructions.s3.amazonaws.com/example_file_1.ts.png"
    )
    assert list(test_data.keys()) == [
        "info",
        "licenses",
        "images",
        "annotations",
        "models",
        "categories",
    ]
