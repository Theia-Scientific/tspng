#!/usr/bin/env python3

import importlib.metadata

from tspng import __app_name__, PNG_FILE_EXT
from tspng.cli import app, map_verbosity
from tspng.schema.ts import v1
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


def test_app_extract_multiple_files(example_file_1_path, example_file_2_path):
    result = runner.invoke(
        app, ["extract", str(example_file_1_path), str(example_file_2_path)]
    )
    assert result.exit_code == 0


def test_app_implant(coco_json_path, empty_png_path):
    expected = empty_png_path.with_suffix(v1.FILE_EXT)
    result = runner.invoke(app, ["implant", str(coco_json_path), str(empty_png_path)])
    assert result.exit_code == 0
    assert expected.exists()
    assert expected.name == empty_png_path.stem + v1.FILE_EXT
    assert expected.suffix == PNG_FILE_EXT
