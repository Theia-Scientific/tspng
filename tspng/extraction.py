#import statements
import io
import json
import os
import warnings

from PIL import Image
from tspng import MIME_TYPE
from typing import Dict, List, Union

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
                Exception: If path is a directory
                Exception: If image is not a PNG
    '''
    #checks if path exists
    if not os.path.exists(path):
        raise Exception(f"{path} does not exist.")
    #check if file exists
    if os.path.isdir(path):
        raise Exception(f"{path} is to a directory.")
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
