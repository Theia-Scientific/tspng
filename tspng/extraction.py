def extraction():

    #import statements
    from PIL import Image

    import json
    import os

    #path to data
    filepath = os.path.dirname(os.path.abspath(__file__))+'/TSDATA'
    #list of files of interest
    filenames = os.listdir(filepath)
    data = []
    for filename in filenames:
        #open
        im = Image.open(filepath+filename)
        meta=im.text
        #load
        dict=json.loads(meta['application/vnd.theiascope.io+json'])
        #append
        data.append(dict)
    return data