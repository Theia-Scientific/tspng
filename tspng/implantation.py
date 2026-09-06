#!/usr/env/bin python3

import logging
import os
import json

from pathlib import Path
from PIL import Image
from PIL.PngImagePlugin import PngInfo
from tspng import MIME_TYPE, PathDoesNotExist, PathIsNotAFile

LOGGER: logging.Logger = logging.getLogger(__name__)


def is_json(data: str) -> bool:
    try:
        json.loads(data)
    except ValueError:
        return False
    return True


def _implant_data(
    data: str,
    image: str | os.PathLike,
    mime_type: str = MIME_TYPE,
    ext: str = ".ts.png",
):
    target_im = Image.open(image)
    metadata = PngInfo()
    metadata.add_text(mime_type, data)
    base, _ = os.path.splitext(image)
    target_im.save(base + ext, format="PNG", pnginfo=metadata)


def implant(
    data: str | os.PathLike, image: str | os.PathLike, mime_type: str = MIME_TYPE
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
        implant_into_file(data, image, mime_type)
    elif isinstance(data, str) and os.path.isfile(data):
        implant_into_file(data, image, mime_type)
    elif isinstance(data, str) and is_json(data):
        _implant_data(data, image, mime_type)
    else:
        raise TypeError("The data is not a JSON file or string.")


def implant_into_file(
    path: str | os.PathLike, image: str | os.PathLike, mime_type: str = MIME_TYPE
):
    """
    Adds data to a PNG image file.

    Parameters:
        path (str, Path): Path to a text or JSON file
        image (str, Path): Path to a PNG file
        mime_type (str): Optional; Media type of file,
            default is 'application/vnd.theiascope.io+json'

    Raises:
        Exception: If path does not exist
        Exception: If path is not a file
        Exception: If text is not JSON
    """
    if not os.path.exists(path):
        LOGGER.warning(f"The '{path}' does not exist.")
        raise PathDoesNotExist(path)
    if not os.path.isfile(path):
        LOGGER.warning(f"The '{path}' is not a file.")
        raise PathIsNotAFile(path)
    data = open(path, "r").read()
    if is_json(data):
        _implant_data(data, image, mime_type)
    else:
        raise TypeError("The data is not a JSON string.")
