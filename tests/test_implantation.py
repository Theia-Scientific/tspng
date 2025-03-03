#!/usr/bin/env python3

import json
import pytest

from pathlib import Path
from tspng import PathDoesNotExist, PathIsNotAFile
from tspng.implantation import implant, implant_into_file
from tspng.extraction import extract

@pytest.fixture
def txt_file_path(tmp_path) -> Path:
    txt_path = tmp_path.joinpath("file.txt")
    with open(txt_path, "w") as f:
        f.write("Hello World! This is NOT JSON.")
    return txt_path


def test_implant_with_path(coco_json_path, empty_png_path):
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


def test_implant_with_str(coco_json_path, empty_png_path):
    implant(str(coco_json_path), str(empty_png_path))
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


def test_implant_with_data(coco_json_path, empty_png_path):
    with open(coco_json_path) as f:
        json_data = json.load(f)
    implant(json.dumps(json_data), str(empty_png_path))
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


def test_implant_fails(empty_png_path):
    with pytest.raises(TypeError):
        implant("Test for failure", empty_png_path)


def test_implant_into_file(coco_json_path, empty_png_path):
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


def test_implant_from_file_fails_with_folder(assets_directory_path, empty_png_path):
    with pytest.raises(PathIsNotAFile):
        implant_into_file(assets_directory_path, empty_png_path)


def test_implant_from_file_fails_existence(empty_png_path):
    with pytest.raises(PathDoesNotExist):
        implant_into_file("tests/assets/no_such_file.json", empty_png_path)

def test_implant_into_file_fails(txt_file_path, empty_png_path):
    with pytest.raises(TypeError):
        implant_into_file(txt_file_path, empty_png_path)
