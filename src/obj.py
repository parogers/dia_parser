
from ns import NS

from attributes import parse_attributes


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


