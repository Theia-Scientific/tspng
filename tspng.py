# extraction.py

import argparse

from tspng.extraction import extract,extract_from_bytes,extract_from_file,extract_from_files,extract_from_folder,extract_from_url

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='For use with TS PNG files')

    #create commands
    parser.add_argument('-extract', help='extract TS PNG metadata')

    #get argument
    args = parser.parse_args()
    if args.extract:
        test = extract(args.extract)
        print(test)
    