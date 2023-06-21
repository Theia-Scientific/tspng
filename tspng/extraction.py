#import statements
from decouple import config
from PIL import Image
#from __init__ import MIME_TYPE

import json
import os

DEFAULT_TSPNG_MIME_TYPE="application/vnd.theiascope.io+json"

MIME_TYPE=(os.environ.get("TSPNG_MIME_TYPE") if os.environ.get("TSPNG_MIME_TYPE") else DEFAULT_TSPNG_MIME_TYPE)

def extract(path):
    #open
    abs_path=os.path.abspath(path)
    im=Image.open(abs_path)
    meta=im.text
    #load
    dict=json.loads(meta[config(MIME_TYPE)])
    return dict
