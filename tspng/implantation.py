#!/usr/env/bin python3

import logging
import os
import json

from pathlib import Path
from PIL import Image
from PIL.PngImagePlugin import PngInfo
from tspng import PathDoesNotExist, PathIsNotAFile
from tspng.schema import Metadata, text

LOGGER: logging.Logger = logging.getLogger(__name__)


def _implant_data(
    metadata: Metadata,
    image: str | os.PathLike,
    default_mime_type: str = text.MIME_TYPE,
):
    LOGGER.debug(f"{metadata=}")
    LOGGER.debug(f"{image=}")
    LOGGER.debug(f"{default_mime_type=}")
    target_im = Image.open(image)
    png_info = PngInfo()
    if metadata.mime_type is None:
        key = default_mime_type
    else:
        key = metadata.mime_type
    LOGGER.debug(f"{key=}")
    png_info.add_text(key, metadata.text)
    base, _ = os.path.splitext(image)
    target_im.save(base + metadata.ext, format="PNG", pnginfo=metadata)


def implant(
    data: Metadata | str | os.PathLike,
    image: str | os.PathLike,
):
    """
    Adds data to a PNG image.

    Parameters:
        data (str, Path): Path to a file or text
        image (str, path): Path to a PNG file
        mime_type (str): Optional; Media type of file,
            default is 'application/vnd.theiascope.io+json'

    Raises:
        TypeError: If data is not a path to a file or a string.
    """
    if isinstance(data, Path) and os.path.isfile(data):
        implant_into_file(data, image)
    elif isinstance(data, str) and os.path.isfile(data):
        implant_into_file(data, image)
    elif isinstance(data, Metadata):
        _implant_data(data, image)
    else:
        raise TypeError("The data is not a JSON file or string.")


def implant_into_file(path: str | os.PathLike, image: str | os.PathLike):
    """
    Adds data to a PNG image file.

    Parameters:
        path (str, Path): Path to a text or JSON file
        image (str, Path): Path to a PNG file

    Raises:
        Exception: If path does not exist
        Exception: If path is not a file
    """
    if not os.path.exists(path):
        LOGGER.warning(f"The '{path}' does not exist.")
        raise PathDoesNotExist(path)
    if not os.path.isfile(path):
        LOGGER.warning(f"The '{path}' is not a file.")
        raise PathIsNotAFile(path)
    text = open(path, "r").read()
    try:
        data = json.loads(text)
    except ValueError:
        data = text
    _implant_data(Metadata(data=data), image)
