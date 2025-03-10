import io
import logging
import json
import os
import urllib.request

from pathlib import Path
from PIL import Image
from tspng import MIME_TYPE, PathDoesNotExist, PathIsNotAFile
from typing import Dict, List, Union
from urllib.parse import urlparse

class NotPngFormat(Exception):
    def __init__(self, im: Image.Image):
        self.image = im

class PathIsNotADir(Exception):
    def __init__(self, path: Union[Path, str]):
        self.path = path

class PathDoesNotContainPngs(Exception):
     def __init__(self, path: Union[Path, str]):
        self.path = path


def _open_image(
    file_or_bytes: Union[Path, str, io.BytesIO], mime_type: str = MIME_TYPE
) -> Dict:
    logging.debug(f"file_or_bytes={file_or_bytes}")
    logging.debug(f"mime_type={mime_type}")
    # open
    im = Image.open(file_or_bytes)
    if im.format != "PNG":
        raise NotPngFormat(im)
    meta = im.text  # pyright: ignore
    # load
    if mime_type in meta.keys():
        d = json.loads(meta[mime_type])
    else:
        logging.warning("There is no embedded TS metadata.")
        d = {}
    return d


def extract(
    file_bytes_files_or_url: Union[str, Path, io.BytesIO, List[Union[str, Path]]],
    mime_type: str = MIME_TYPE,
) -> Dict:
    """
    Returns the metadata from a TSPNG file as a dictionary.

        Parameters:
                file_bytes_or_files (str, io.BytesIO, List[str]): Path to a file, byte stream, or files
                mime_type (str): Optional; Media type of file,
                    default is 'application/vnd.theiascope.io+json'

        Returns:
                (dict): Dictionary containing file metadata

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
    elif isinstance(file_bytes_files_or_url, List):
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


def extract_from_bytes(buffer: io.BytesIO, mime_type: str = MIME_TYPE) -> Dict:
    """
    Returns the metadata from a TS byte stream as a dictionary.

        Parameters:
                buffer (BytesIO): Path to a byte stream
                mime_type (str): Optional; Media type of file,
                    default is 'application/vnd.theiascope.io+json'

        Returns:
                (dict): Dictionary containing file metadata

        Raises:
                TypeError: If buffer is not BytesIO
                Exception: If image is not a PNG
    """
    return _open_image(buffer, mime_type)


def extract_from_file(path: Union[Path, str], mime_type: str = MIME_TYPE) -> Dict:
    """
    Returns the metadata from a TSPNG file as a dictionary.

        Parameters:
                path (str): Path to a file as a string
                mime_type (str): Optional; Media type of file,
                    default is 'application/vnd.theiascope.io+json'

        Returns:
                (dict): Dictionary containing file metadata

        Raises:
                Exception: If path does not exist
                Exception: If path is not a file
                Exception: If image is not a PNG
    """
    if not os.path.exists(path):
        raise PathDoesNotExist(path)
    if not os.path.isfile(path):
        raise PathIsNotAFile(path)
    return _open_image(path, mime_type)


def extract_from_files(
    paths: List[Union[str, Path]], mime_type: str = MIME_TYPE
) -> Dict:
    """
    Returns a nested dictionary of metadata from a list of TSPNG file paths.

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


def extract_from_folder(path: Union[str, Path], mime_type: str = MIME_TYPE) -> Dict:
    """
    Returns a nested dictionary of metadata from a folder of TSPNG file paths.

        Parameters:
                path (str): A path to a folder
                mime_type (str): Optional; Media type of file,
                    default is 'application/vnd.theiascope.io+json'

        Returns:
                (dict): Dictionary containing metadata of each file

        Raises:
                Exception: If path is not a directory
                Exception: If path does not contain a PNG file
    """
    # check if directory
    if not os.path.isdir(path):
        raise PathIsNotADir(path)
    # return all files as a list
    file_list = []
    for file in os.listdir(path):
        # check the files which end with a specific extension
        root_ext = os.path.splitext(file)
        if root_ext[1] == ".png":
            # print path name of selected files
            file_list.append(os.path.join(path, file))
    # check if any PNG files in directory
    if file_list == []:
        raise PathDoesNotContainPngs(path)
    return extract_from_files(file_list, mime_type)


def extract_from_url(url: str, mime_type: str = MIME_TYPE) -> Dict:
    """
    Returns the metadata from a TS url as a dictionary.

        Parameters:
                url (str): URL to a TS PNG file
                mime_type (str): Optional; Media type of file,
                    default is 'application/vnd.theiascope.io+json'

        Returns:
                (dict): Dictionary containing file metadata

        Raises:
                Exception: If cannot get image from url
    """
    response = urllib.request.urlopen(url)
    img_data = response.read()
    return _open_image(io.BytesIO(img_data), mime_type)
