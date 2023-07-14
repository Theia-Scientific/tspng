#import statements
import json
import os

from PIL import Image
from tspng import MIME_TYPE
from typing import List

def extract_from_file(path: str, mime_type: str=MIME_TYPE):
    '''
    Returns the metadata from a TSPNG file as a dictionary.

        Parameters:
                path (str): Path to a file as a string
                mime_type (str): Optional; Media type of file,
                    default is 'application/vnd.theiascope.io+json'

        Returns:
                dict (dict): Dictionary containing file metadata
    '''
    #open
    abs_path=os.path.abspath(path)
    im=Image.open(abs_path)
    meta=im.text
    #load
    dict=json.loads(meta[mime_type])
    return dict

def extract_from_files(paths: List, mime_type: str=MIME_TYPE):
    '''
    Returns a nested dictionary of metadata from a list of TSPNG file paths.

        Parameters:
                path (list[str]): List of file paths
                mime_type (str): Optional; Media type of file,
                    default is 'application/vnd.theiascope.io+json'

        Returns:
                nested_dict (dict): Dictionary containing metadata of each file
    '''
    nested_dict = {}
    for path in paths:
        nested_dict[path] = extract_from_file(path, mime_type)
    return nested_dict
