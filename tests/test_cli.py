#!/usr/bin/env python3

import importlib.metadata

from tspng import __app_name__
from tspng.cli import app, map_verbosity
from typer.testing import CliRunner

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
