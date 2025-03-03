#!/usr/bin/env python3

import pytest

from io import BytesIO
from pathlib import Path
from PIL import Image
from tspng.extraction import (
    _open_image,
    extract,
    extract_from_bytes,
    extract_from_file,
    extract_from_files,
    extract_from_folder,
    extract_from_url,
    NotPngFormat,
    PathDoesNotContainPngs,
    PathDoesNotExist,
    PathIsNotADir,
    PathIsNotAFile
)
from urllib.error import HTTPError

@pytest.fixture
def empty_jpeg_path(tmp_path) -> Path:
    empty_jpeg_path = tmp_path.joinpath("empty.jpeg")
    image = Image.new('RGB', (640, 640))
    image.save(empty_jpeg_path, format="JPEG")
    return empty_jpeg_path

@pytest.fixture
def example_file_1_url() -> str:
    return "https://bounding-box-instructions.s3.amazonaws.com/example_file_1.ts.png"

def test_extract_with_file_path(example_file_1_path):
    test_data = extract(example_file_1_path)
    assert list(test_data.keys()) == [
        "info",
        "licenses",
        "images",
        "annotations",
        "models",
        "categories",
    ]


def test_extract_with_file_str(example_file_1_path):
    test_data = extract(str(example_file_1_path))
    assert list(test_data.keys()) == [
        "info",
        "licenses",
        "images",
        "annotations",
        "models",
        "categories",
    ]


def test_extract_with_files(example_file_1_path, example_file_2_path):
    files = [
        example_file_1_path,
        example_file_2_path,
    ]
    test_data = extract(files)
    assert list(test_data.keys()) == files


def test_extract_with_folder(assets_directory_path, example_file_1_path, example_file_2_path):
    test_data = extract(assets_directory_path)
    assert str(example_file_1_path) in sorted(list(test_data.keys()))
    assert str(example_file_2_path) in sorted(list(test_data.keys()))


def test_extract_with_url(example_file_1_url):
    test_data = extract(example_file_1_url)
    assert list(test_data.keys()) == [
        "info",
        "licenses",
        "images",
        "annotations",
        "models",
        "categories",
    ]


def test_extract_with_bytes(example_file_1_path):
    with open(example_file_1_path, "rb") as fh:
        buf = BytesIO(fh.read())
    test_data = extract(buf)
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


def test_extract_from_bytes(example_file_1_path):
    """
    Tests the dictionary keys from an example TS byte stream.
    """
    with open(example_file_1_path, "rb") as fh:
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


def test_extract_from_file(example_file_1_path):
    """
    Tests the dictionary keys from an example TSPNG file path.
    """
    test_data = extract_from_file(example_file_1_path)
    assert list(test_data.keys()) == [
        "info",
        "licenses",
        "images",
        "annotations",
        "models",
        "categories",
    ]


def test_extract_from_file_not_exists_fails():
    with pytest.raises(PathDoesNotExist):
        extract_from_file(Path("Random/path.png"))


def test_extract_from_file_with_directory_fails(assets_directory_path):
    with pytest.raises(PathIsNotAFile):
        extract_from_file(assets_directory_path)


def test_extract_from_files(example_file_1_path, example_file_2_path):
    """
    Tests the dictionary keys from a list of example TSPNG file paths.
    """
    files = [
            example_file_1_path,
            example_file_2_path,
        ]
    test_data = extract_from_files(files)
    assert sorted(list(test_data.keys())) == files


def test_extract_from_folder(assets_directory_path, example_file_1_path, example_file_2_path):
    """
    Tests the dictionary keys from a list of example TSPNG file paths.
    """
    test_data = extract_from_folder(assets_directory_path)
    assert str(example_file_1_path) in sorted(list(test_data.keys()))
    assert str(example_file_2_path) in sorted(list(test_data.keys()))


def test_extract_from_folder_fails(example_file_1_path):
    with pytest.raises(PathIsNotADir):
        extract_from_folder(example_file_1_path)


def test_extract_from_folder_fails_with_empty_files(tmp_path):
    with pytest.raises(PathDoesNotContainPngs):
        extract_from_folder(tmp_path)


def test_extract_from_url(example_file_1_url):
    """
    Tests the dictionary keys from an example TSPNG url.
    """
    test_data = extract_from_url(example_file_1_url)
    assert list(test_data.keys()) == [
        "info",
        "licenses",
        "images",
        "annotations",
        "models",
        "categories",
    ]


def test_extract_from_url_fails():
    with pytest.raises(HTTPError):
        extract_from_url("https://bounding-box-instructions.s3.amazonaws.com/example_file_4.ts.png")


def test_open_image_not_png_fails(empty_jpeg_path):
    with pytest.raises(NotPngFormat):
        _open_image(empty_jpeg_path)


def test_empty_embedded_data(empty_png_path):
    result = _open_image(empty_png_path)
    assert result == {}
