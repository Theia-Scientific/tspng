#!/usr/bin/env python3

from tspng.extraction import extract

def test_hello_world():
    print('Hello World!')

def test_extraction():
    test_data = extract('tests/assets/example_file.ts.png')
    assert list(test_data.keys())==['info','licenses','images','annotations','models','categories']
