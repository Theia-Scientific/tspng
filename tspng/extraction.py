#!/usr/env/bin python3

import io
import logging
import json
import os
import urllib.request

from pathlib import Path
from PIL import Image
from PIL.PngImagePlugin import PngImageFile
from tspng import MIME_TYPE, PathDoesNotExist, PathIsNotAFile
from tspng.schema.ts import Version1 as TsJson
from typing import Any
from urllib.parse import urlparse

LOGGER: logging.Logger = logging.getLogger(__name__)


class NotPngFormat(Exception):
    def __init__(self, im: Image.Image):
        self.image = im


class PathIsNotADir(Exception):
    def __init__(self, path: str | os.PathLike):
        self.path = path


class PathDoesNotContainPngs(Exception):
    def __init__(self, path: str | os.PathLike):
        self.path = path


def _open_image(
    file_or_bytes: str | os.PathLike | io.BytesIO, mime_type: str = MIME_TYPE
) -> dict[str, Any] | None:
    LOGGER.debug(f"{file_or_bytes=}")
    LOGGER.debug(f"{mime_type=}")
    im = Image.open(file_or_bytes)
    if not isinstance(im, PngImageFile):
        raise NotPngFormat(im)
    meta = im.text
    if meta is None:
        LOGGER.warning("There is no metadata.")
        return None
    if mime_type in meta.keys():
        d = json.loads(meta[mime_type])
    else:
        LOGGER.warning("There is no embedded TS metadata.")
        d = None
    return d


def extract(
    file_bytes_files_or_url: str | os.PathLike | io.BytesIO | list[str | os.PathLike],
    mime_type: str = MIME_TYPE,
) -> TsJson | dict[str | os.PathLike, TsJson]:
    """
    Returns the metadata from a TS PNG file as either a dictionary-like object
    if a single file is extracted or a dictionary with the keys as the paths to
    the files if multiple files are extracted.

    Parameters:
        file_bytes_or_files (str, Path, io.BytesIO, List[str]): Path to a file,
            byte stream, or files
        mime_type (str): Optional; Media type of file,
            default is 'application/vnd.theiascope.io+json'

    Returns:
        (TsJson, dict): A dictionary-like object or a dictionary with the keys
            as the paths to the files and the values as a dictionary-like object
            containing the metadata

    Raises:
        TypeError: If not a BytesIO object, file, list of files, or folder
    """
    # call appropriate function
    if isinstance(file_bytes_files_or_url, io.BytesIO):
        return extract_from_bytes(file_bytes_files_or_url, mime_type)
    elif isinstance(file_bytes_files_or_url, str) and os.path.isfile(
        file_bytes_files_or_url
    ):
        return extract_from_file(file_bytes_files_or_url, mime_type)
    elif isinstance(file_bytes_files_or_url, Path) and os.path.isfile(
        file_bytes_files_or_url
    ):
        return extract_from_file(file_bytes_files_or_url, mime_type)
    elif isinstance(file_bytes_files_or_url, list):
        return extract_from_files(file_bytes_files_or_url, mime_type)
    elif isinstance(file_bytes_files_or_url, Path) and os.path.isdir(
        file_bytes_files_or_url
    ):
        return extract_from_folder(Path(file_bytes_files_or_url), mime_type)
    elif urlparse(str(file_bytes_files_or_url))[0] != "":
        return extract_from_url(str(file_bytes_files_or_url), mime_type)
    else:
        raise TypeError(
            f"{file_bytes_files_or_url} is not a BytesIO object, file, list of files, or folder."
        )


def extract_from_bytes(buffer: io.BytesIO, mime_type: str = MIME_TYPE) -> TsJson:
    """
    Returns the metadata from a TS PNG byte stream as a dictionary-like object.

    Parameters:
        buffer (BytesIO): Path to a byte stream
        mime_type (str): Optional; Media type of file,
            default is 'application/vnd.theiascope.io+json'

    Returns:
        (TsJson): A dictionary-like object containing the metadata from the TS
            PNG file

    Raises:
        TypeError: If buffer is not BytesIO
        Exception: If image is not a PNG
    """
    return TsJson.model_validate(_open_image(buffer, mime_type))


def extract_from_file(path: str | os.PathLike, mime_type: str = MIME_TYPE) -> TsJson:
    """
    Returns the metadata from a TS PNG file as a dictionary-like object.

    Parameters:
        path (str): Path to a file as a string
        mime_type (str): Optional; Media type of file,
            default is 'application/vnd.theiascope.io+json'

    Returns:
        (TsJson): A dictionary-like object containing the TS PNG file metadata

    Raises:
        Exception: If path does not exist
        Exception: If path is not a file
        Exception: If image is not a PNG
    """
    if not os.path.exists(path):
        raise PathDoesNotExist(path)
    if not os.path.isfile(path):
        raise PathIsNotAFile(path)
    return TsJson.model_validate(_open_image(path, mime_type))


def extract_from_files(
    paths: list[str | os.PathLike], mime_type: str = MIME_TYPE
) -> dict[str | os.PathLike, TsJson]:
    """
    Returns a dictionary of dictionary-like objects from a list of TS PNG file
    paths, where the keys are the paths to the files.

    Parameters:
        path (list[str]): List of file paths
        mime_type (str): Optional; Media type of file,
            default is 'application/vnd.theiascope.io+json'

    Returns:
        (dict): Dictionary containing metadata of each file
    """
    nested_dict = {}
    for path in paths:
        nested_dict[path] = extract_from_file(path, mime_type)
    return nested_dict


def extract_from_folder(
    path: str | os.PathLike, mime_type: str = MIME_TYPE
) -> dict[str | os.PathLike, TsJson]:
    """
    Returns a dictionary of dictionary-like objects containing the metadata from
    a folder of TS PNG file paths. The keys are the file paths.

    Parameters:
        path (str): A path to a folder
        mime_type (str): Optional; Media type of file,
            default is 'application/vnd.theiascope.io+json'

    Returns:
        (TsJson): A dictionary-like object containing the metadata of each file

    Raises:
        Exception: If path is not a directory
        Exception: If path does not contain a PNG file
    """
    if not os.path.isdir(path):
        raise PathIsNotADir(path)
    file_list = []
    for file in os.listdir(path):
        root_ext = os.path.splitext(file)
        if root_ext[1] == ".png":
            file_list.append(os.path.join(path, file))
    if file_list == []:
        raise PathDoesNotContainPngs(path)
    return extract_from_files(file_list, mime_type)


def extract_from_url(url: str, mime_type: str = MIME_TYPE) -> TsJson:
    """
    Returns the metadata from a TS PNG URL as a TS PNG JSON object.

        Parameters:
                url (str): URL to a TS PNG file
                mime_type (str): Optional; Media type of file,
                    default is 'application/vnd.theiascope.io+json'

        Returns:
                (TsJson): An dictionary-like object containing the file metadata

        Raises:
                Exception: If the image cannot be obtained from the URL
    """
    response = urllib.request.urlopen(url)
    img_data = response.read()
    return TsJson.model_validate(_open_image(io.BytesIO(img_data), mime_type))
