#import statements
from PIL import Image
from tspng import MIME_TYPE

import json
import os

def extract(path):
    #open
    abs_path=os.path.abspath(path)
    im=Image.open(abs_path)
    meta=im.text
    #load
    dict=json.loads(meta[MIME_TYPE])
    return dict
