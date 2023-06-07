#import statements
from PIL import Image

import json

def extraction(fname):
    #open
    im=Image.open(fname)
    meta=im.text
    #load
    dict=json.loads(meta['application/vnd.theiascope.io+json'])
    return dict
