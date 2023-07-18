#import statements
import json
import os

from PIL import Image
from tspng import MIME_TYPE
from typing import Dict, List

def extract_from_file(path: str, mime_type: str=MIME_TYPE) -> Dict:
    '''
    Returns the metadata from a TSPNG file as a dictionary.

        Parameters:
                path (str): Path to a file as a string
                mime_type (str): Optional; Media type of file,
                    default is 'application/vnd.theiascope.io+json'

        Returns:
                dict (dict): Dictionary containing file metadata
    '''
    #checks if path exists
    if os.path.exists(path)==False:
        raise Exception(f"{path} does not exist.")
    #check if file is TSPNG file
    fname = os.path.split(os.path.abspath(path))[1]
    if fname[-6:] != 'ts.png':
        raise TypeError(f"{fname} is not a TSPNG file.")
    #open
    im=Image.open(path)
    meta=im.text
    #load
    dict=json.loads(meta[mime_type])
    return dict

def extract_from_files(paths: List, mime_type: str=MIME_TYPE) -> Dict:
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
