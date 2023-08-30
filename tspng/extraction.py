#import statements
import io
import json
import os
import pathlib
import warnings
import urllib.request

from PIL import Image
from tspng import MIME_TYPE
from typing import Dict, List, Union
from urllib.parse import urlparse

def _open_image(file_or_bytes: Union[str, io.BytesIO], mime_type: str=MIME_TYPE) -> Dict:
    #open
    im=Image.open(file_or_bytes)
    if im.format != 'PNG':
        raise Exception("Image is not a PNG.")
    meta=im.text
    #load
    if mime_type in meta.keys():
        d=json.loads(meta[mime_type])
    else:
        #warn if file has no embedded data
        warnings.warn(f"{file_or_bytes} has no embedded TS metadata.")
        d={}
    return d

def extract(file_bytes_files_or_url: Union[str, io.BytesIO, List[str]], mime_type: str=MIME_TYPE) -> Dict:
    '''
    Returns the metadata from a TSPNG file as a dictionary.

        Parameters:
                file_bytes_or_files (str, io.BytesIO, List[str]): Path to a file, byte stream, or files
                mime_type (str): Optional; Media type of file,
                    default is 'application/vnd.theiascope.io+json'

        Returns:
                (dict): Dictionary containing file metadata

        Raises:
                TypeError: If not a BytesIO object, file, list of files, or folder
    '''
    #call appropriate function
    if isinstance(file_bytes_files_or_url, io.BytesIO):
        return extract_from_bytes(file_bytes_files_or_url, MIME_TYPE)
    elif type(file_bytes_files_or_url) == str and os.path.isfile(file_bytes_files_or_url):
        return extract_from_file(file_bytes_files_or_url, MIME_TYPE)
    elif isinstance(file_bytes_files_or_url, list):
        return extract_from_files(file_bytes_files_or_url, MIME_TYPE)
    elif os.path.isdir(file_bytes_files_or_url):
        return extract_from_folder(file_bytes_files_or_url, MIME_TYPE)
    elif urlparse(file_bytes_files_or_url)[0] != '':
        return extract_from_url(file_bytes_files_or_url, MIME_TYPE)
    else:
        raise TypeError(f"{file_bytes_files_or_url} is not a BytesIO object, file, list of files, or folder.")

def extract_from_bytes(buffer: io.BytesIO, mime_type: str=MIME_TYPE) -> Dict:
    '''
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
    '''
    #check if file is BytesIO
    if not isinstance(buffer, io.BytesIO):
        raise TypeError(f"{buffer} is not a BytesIO object.")
    return _open_image(buffer,mime_type)

def extract_from_file(path: str, mime_type: str=MIME_TYPE) -> Dict:
    '''
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
    '''
    #checks if path exists
    if not os.path.exists(path):
        raise Exception(f"{path} does not exist.")
    #check if file exists
    if not os.path.isfile(path):
        raise Exception(f"The {path} is not a file.")
    return _open_image(path,mime_type)

def extract_from_files(paths: List[str], mime_type: str=MIME_TYPE) -> Dict:
    '''
    Returns a nested dictionary of metadata from a list of TSPNG file paths.

        Parameters:
                path (list[str]): List of file paths
                mime_type (str): Optional; Media type of file,
                    default is 'application/vnd.theiascope.io+json'

        Returns:
                (dict): Dictionary containing metadata of each file
    '''
    nested_dict = {}
    for path in paths:
        nested_dict[path] = extract_from_file(path, mime_type)
    return nested_dict

def extract_from_folder(path: str, mime_type: str=MIME_TYPE) -> Dict:
    '''
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
    '''
    #check if directory
    if not os.path.isdir(path):
        raise Exception(f"The {path} is not to a directory.")
    # return all files as a list
    file_list = []
    for file in os.listdir(path):
        # check the files which are end with specific extension
        root_ext = os.path.splitext(file)
        if root_ext[1] == '.png':
            # print path name of selected files
            file_list.append(os.path.join(path, file))
    #check if any PNG files in directory
    if file_list == []:
        raise Exception(f"The {path} does not contain a PNG file.")
    return extract_from_files(file_list, mime_type)

def extract_from_url(url: str, mime_type: str=MIME_TYPE) -> Dict:
    '''
    Returns the metadata from a TS byte stream as a dictionary.

        Parameters:
                url (str): URL to a TS PNG file
                mime_type (str): Optional; Media type of file,
                    default is 'application/vnd.theiascope.io+json'

        Returns:
                (dict): Dictionary containing file metadata
    '''
    urllib.request.urlretrieve(url,'url')
    return _open_image('url',mime_type)
