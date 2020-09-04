#!/usr/bin/env python3

import sys

import site
site.addsitedir('src')
from dia_parser import parse_dia_file

if __name__ == '__main__':
    diagram = parse_dia_file(sys.argv[1])
    for layer in diagram.layers:
        print(layer.name)
        for obj in layer.iter_objects():
            print('   ', obj.obj_id, obj)

