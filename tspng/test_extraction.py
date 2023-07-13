#!/usr/bin/env python3

from tspng.extraction import extract_from_file

def test_hello_world():
    print('Hello World!')

def test_extract_from_file():
    test_data = extract_from_file('tests/assets/example_file.ts.png')
    assert list(test_data.keys())==['info','licenses','images','annotations','models','categories']
