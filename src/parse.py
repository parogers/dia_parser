#!/usr/bin/env python3

import gzip
import sys
from xml.etree import ElementTree

from attributes import parse_attributes
from obj import parse_object
from ns import NS

def parse_diagramdata(diagramdata_node):
    data = DiagramData()
    data.attributes = parse_attributes(diagramdata_node)
    return data


def parse_layer(layer_node):
    layer = Layer()
    layer.name = layer_node.attrib['name']
    layer.visible = layer_node.attrib['visible'] == 'true'
    layer.connectable = layer_node.attrib['connectable'] == 'true'
    layer.active = layer_node.attrib['active'] == 'true'
    for obj_node in layer_node.findall(NS + 'object'):
        obj = parse_object(obj_node, layer)
        layer.objects.append(obj)
    return layer


def parse_diagram(diagram_node):
    diagram = Diagram()

    node = diagram_node.find(NS + 'diagramdata')
    if node:
        diagram.diagram_data = parse_diagramdata(node)


    for layer_node in diagram_node.findall(NS + 'layer'):
        layer = parse_layer(layer_node)
        diagram.layers.append(layer)
    return diagram



class Layer:
    name = ''

    def __init__(self):
        self.objects = []

    def __getitem__(self, obj_id):
        try:
            return next(filter(
                lambda obj : obj.obj_id == obj_id, self.objects
            ))
        except StopIteration:
            raise KeyError

    def iter_line_objects(self):
        return filter(
            lambda obj : obj.is_line,
            self.iter_objects()
        )

    def iter_objects(self):
        # TODO - handle groups
        return iter(self.objects)


class Diagram:
    layers = None

    def __init__(self):
        self.layers = []

    def __getitem__(self, name):
        try:
            return next(filter(
                lambda layer : layer.name == name, self.layers
            ))
        except StopIteration:
            raise KeyError


class DiagramData:
    attributes = None


def read_gzip_file(src):
    return gzip.open(src).read()

def read_dia_file(src):
    '''Reads a .dia file (compressed or uncompressed) and returns the XML data as a string'''

    try:
        xml_data = read_gzip_file(src)
    except OSError:
        xml_data = open(src, 'rb').read()

    xml_data = xml_data.decode('utf-8')
    assert xml_data.lower().startswith('<?xml'), 'not a valid xml file'
    return xml_data

def parse_dia_file(src):
    xml_data = read_dia_file(src)

    root = ElementTree.fromstring(xml_data)
    assert root.tag == NS + 'diagram'

    return parse_diagram(root)


diagram = parse_dia_file(sys.argv[1])
for layer in diagram.layers:
    print(layer.name)
    for obj in layer.iter_objects():
        print('   ', obj.obj_id, obj)

