#!/usr/bin/env python3

import pytest

from pathlib import Path
from PIL import Image


@pytest.fixture
def assets_directory_path(request) -> Path:
    return Path(request.config.rootdir).joinpath("tests", "assets")


@pytest.fixture
def example_file_1_path(assets_directory_path) -> Path:
    return assets_directory_path.joinpath("example_file_1.ts.png")


@pytest.fixture
def example_file_2_path(assets_directory_path) -> Path:
    return assets_directory_path.joinpath("example_file_2.ts.png")


@pytest.fixture
def coco_json_path(assets_directory_path) -> Path:
    return assets_directory_path.joinpath("coco_data.json")


@pytest.fixture
def ts_v1_legacy_json_path(assets_directory_path) -> Path:
    return assets_directory_path.joinpath("ts_v1_legacy_data.json")


@pytest.fixture
def ts_v1_modern_json_path(assets_directory_path) -> Path:
    return assets_directory_path.joinpath("ts_v1_modern_data.json")


@pytest.fixture
def empty_png_path(tmp_path) -> Path:
    empty_png_path = tmp_path.joinpath("empty.png")
    image = Image.new("RGB", (640, 640))
    image.save(empty_png_path, format="PNG")
    return empty_png_path


@pytest.fixture
def txt_file_path(tmp_path) -> Path:
    txt_path = tmp_path.joinpath("file.txt")
    with open(txt_path, "w") as f:
        f.write("Hello World! This is NOT JSON.")
    return txt_path
