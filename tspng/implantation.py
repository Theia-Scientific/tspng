#!/usr/env/bin python3

import io
import logging
import os

from PIL import Image
from PIL.PngImagePlugin import PngInfo
from tspng.schema import Metadata, text

LOGGER: logging.Logger = logging.getLogger(__name__)


def implant(
    data: Metadata | os.PathLike[str],
    src: os.PathLike[str] | io.BytesIO | Image.Image,
    dst: os.PathLike[str] | io.BytesIO,
    default_mime_type: str = text.MIME_TYPE,
):
    """
    Adds data to a PNG image.

    Parameters:
        data (Metadata, str, os.PathLike, bytes): Dictionary-like object to
            implant in an image or the path to a file to load or a bytes.
        src (str, path, io.BytesIO, Image.Image): The source image.
        dst (str, path, io.BytesIO): The destination image.
    """
    LOGGER.debug(f"{data=}")
    LOGGER.debug(f"{src=}")
    LOGGER.debug(f"{dst=}")
    if isinstance(data, os.PathLike):
        metadata = Metadata.load(data)
    else:
        metadata = data
    png_info = PngInfo()
    if metadata.mime_type is None:
        key = default_mime_type
    else:
        key = metadata.mime_type
    LOGGER.debug(f"{key=}")
    png_info.add_text(key, metadata.text)
    LOGGER.debug(f"{png_info=}")
    if (
        isinstance(src, str)
        or isinstance(src, os.PathLike)
        or isinstance(src, io.BytesIO)
    ):
        target_im = Image.open(src)
    else:
        target_im = src
    target_im.save(dst, format="PNG", pnginfo=png_info)


def implant_into_file(
    data: Metadata | os.PathLike[str],
    src: os.PathLike[str] | io.BytesIO | Image.Image,
    dst: os.PathLike[str],
    default_mime_type: str = text.MIME_TYPE,
):
    """
    Adds data to a PNG image file.

    Parameters:
        data (Metadata, str, os.PathLike, bytes): Dictionary-like object to
            implant in an image or the path to a file to load or a bytes.
        src (str, path, io.BytesIO, Image.Image): The source image.
        dst (str, path): The destination image.
    """
    implant(data, src, dst, default_mime_type=default_mime_type)


def implant_into_bytes(
    data: Metadata | os.PathLike[str],
    src: os.PathLike[str] | io.BytesIO | Image.Image,
    dst: io.BytesIO,
    default_mime_type: str = text.MIME_TYPE,
):
    """
    Adds data to a buffer as a PNG image.

    Parameters:
        data (Metadata, str, os.PathLike, bytes): Dictionary-like object to
            implant in an image or the path to a file to load or a bytes.
        src (str, path, io.BytesIO, Image.Image): The source image.
        dst (io.BytesIO): The buffer.
    """
    implant(data, src, dst, default_mime_type=default_mime_type)
