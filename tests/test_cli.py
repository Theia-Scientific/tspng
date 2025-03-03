#!/usr/bin/env python3

import importlib.metadata
import pytest

from pathlib import Path
from PIL import Image
from tspng import __app_name__
from tspng.cli import app, map_verbosity
from typer.testing import CliRunner

@pytest.fixture
def assets_directory_path(request) -> Path:
    return Path(request.config.rootdir).joinpath("tests", "assets")

@pytest.fixture
def example_file_1_path(assets_directory_path) -> Path:
    return assets_directory_path.joinpath("example_file_1.ts.png")

@pytest.fixture
def coco_json_path(assets_directory_path) -> Path:
    return assets_directory_path.joinpath("coco_data.json")

@pytest.fixture
def empty_png_path(tmp_path) -> Path:
    empty_png_path = tmp_path.joinpath("empty.png")
    image = Image.new('RGB', (640, 640))
    image.save(empty_png_path, format="PNG")
    return empty_png_path


runner = CliRunner()

def test_map_verbosity_false():
    actual = map_verbosity(False)
    assert actual == "INFO"


def test_map_verbosity_true():
    actual = map_verbosity(True)
    assert actual == "DEBUG"


def test_app_help():
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0


def test_app_version():
    version = importlib.metadata.version(__app_name__)
    result = runner.invoke(app, ["--version"])
    assert result.exit_code == 0
    assert f"{__app_name__} {version}" in result.stdout


def test_app_extract(example_file_1_path):
    result = runner.invoke(app, ["extract", str(example_file_1_path)])
    assert result.exit_code == 0


def test_app_implant(coco_json_path, empty_png_path):
    result = runner.invoke(app, ["implant", str(coco_json_path), str(empty_png_path)])
    assert result.exit_code == 0
