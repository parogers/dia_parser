#!/usr/bin/env python3

import gzip
import sys
from xml.etree import ElementTree


NS = '{http://www.lysator.liu.se/~alla/dia/}'

def parse_real(value_node):
    return float(value_node.attrib['val'])

def parse_boolean(value_node):
    return bool(value_node.attrib['val'])

def parse_point(value_node):
    args = value_node.attrib['val'].split(',')
    return (
        float(args[0]),
        float(args[1]),
    )

def parse_rectangle(value_node):
    left, right = value_node.attrib['val'].split(';')
    args1 = left.split(',')
    args2 = right.split(',')
    return (
        float(args1[0]),
        float(args1[1]),
        float(args2[0]),
        float(args2[1]),
    )

def parse_enum(value_node):
    return int(value_node.attrib['val'])

def parse_int(value_node):
    return int(value_node.attrib['val'])

def parse_string(value_node):
    return value_node.text

def parse_color(value_node):
    return value_node.attrib['val']

def parse_font(value_node):
    return (
        value_node.attrib['family'],
        value_node.attrib['style'],
        value_node.attrib['name']
    )

def parse_attribute_value(attrib_node):
    if len(attrib_node) == 0:
        return None

    value_node = list(attrib_node)[0]

    tag = value_node.tag[len(NS):]
    if tag == 'real':
        return parse_real(value_node)
    elif tag == 'boolean':
        return parse_boolean(value_node)
    elif tag == 'point':
        return parse_point(value_node)
    elif tag == 'rectangle':
        return parse_rectangle(value_node)
    elif tag == 'enum':
        return parse_enum(value_node)
    elif tag == 'composite':
        return parse_attributes(value_node)
    elif tag == 'string':
        return parse_string(value_node)
    elif tag == 'color':
        return parse_color(value_node)
    elif tag == 'font':
        return parse_font(value_node)
    elif tag == 'int':
        return parse_int(value_node)

    print('unknown tag', tag)

    return ''

def parse_attributes(parent_node):
    attributes = {}

    for attrib_node in parent_node.findall(NS + 'attribute'):
        name = attrib_node.attrib['name']
        try:
            avalue = parse_attribute_value(attrib_node)
        except Exception as ex:
            print('error parsing attribute value for', name, ':', ex)
            raise

        attributes[name] = avalue

    return attributes


def parse_diagramdata(diagramdata_node):
    data = DiagramData()
    data.attributes = parse_attributes(diagramdata_node)
    return data


def parse_connection(conn_node, layer):
    conn = Connection(layer)
    conn.handle = conn_node.attrib['handle']
    conn.to_id = conn_node.attrib['to']
    conn.connection = conn_node.attrib['connection']
    return conn


def parse_connections(obj_node, layer):
    connections_node = obj_node.find(NS + 'connections')
    if not connections_node:
        return []

    return [
        parse_connection(conn_node, layer)
        for conn_node in connections_node.findall(NS + 'connection')
    ]


def parse_object(obj_node, layer):
    obj = Object(layer)
    obj.obj_id = obj_node.attrib['id']
    obj.obj_type = obj_node.attrib['type']
    obj.version = obj_node.attrib['version']
    obj.attributes = parse_attributes(obj_node)
    obj.connections = parse_connections(obj_node, layer)
    return obj


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


class AttribValue:
    value_type = None
    value = None

    def __repr__(self):
        return self.value_type + '/' + self.value


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


class Object:
    obj_id = ''
    obj_type = ''
    version = ''
    attributes = None
    connections = None
    layer = None

    def __init__(self, layer):
        self.layer = layer

    def __repr__(self):
        return '<Object id="{}" type="{}" version="{}">'.format(
            self.obj_id,
            self.obj_type,
            self.version
        )

    @property
    def connection_to(self):
        assert self.is_line
        return self.connections[1]

    @property
    def connection_from(self):
        assert self.is_line
        return self.connections[0]

    @property
    def is_line(self):
        return self.connections and len(self.connections) == 2

    @property
    def connected_via(self):
        return list(
            map(
                lambda obj : obj.connection_to,
                filter(
                    lambda obj : obj.connection_from.to_id == self.obj_id,
                    self.layer.iter_line_objects()
                )
            )
        )


class Connection:
    handle = ''
    to_id = ''
    connection = ''
    layer = None

    def __init__(self, layer):
        self.layer = layer

    @property
    def to(self):
        return self.layer[self.to_id]


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

