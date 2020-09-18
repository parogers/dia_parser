#
# dia_parser - A module for parsing dia diagram files
# Copyright (C) 2020  Peter Rogers (peter.rogers@gmail.com)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#

from .ns import NS
from .attributes import parse_attributes


class LineComponent:
    def __init__(self, obj):
        self.obj = obj

    @property
    def connection_to(self):
        '''The connection representing the head of this line object (throws AssertionError if not a line)'''

        if self.obj.attributes.get('bez_points'):
            handle = 3
        elif self.obj.attributes.get('poly_points'):
            # The last handle is the "to" connection, except for #0 which is always "from"
            handles = sorted(self.obj.connections_by_handle.keys())
            if not handles:
                return None
            handle = handles[-1]
            if handle == 0:
                return None
        else:
            handle = 1

        return self.obj.connections_by_handle.get(handle)

    @property
    def connection_from(self):
        '''The connection representing the tail of this line object (throws AssertionError if not a line)'''

        return self.obj.connections_by_handle.get(0)

    @property
    def connected_to(self):
        '''The object pointed to by the head of this line (throws AssertionError if not a line)'''

        return self.connection_to and self.connection_to.to

    @property
    def connected_from(self):
        '''The object pointed to by the tail of this line (throws AssertionError if not a line)'''

        return self.connection_from and self.connection_from.to


class Node:
    '''A node is the common base class to a dia object, and a dia group'''

    parent = None

    @property
    def layer(self):
        '''The layer containing this object'''

        node = self.parent
        while node:
            if hasattr(node, 'is_layer') and node.is_layer:
                return node
            if not hasattr(node, 'parent'):
                break
            node = node.parent
        return None

    @property
    def diagram(self):
        '''The diagram containing this object'''

        if self.layer:
            return self.layer.diagram
        return None


class Object(Node):
    obj_id = ''
    obj_type = ''
    version = ''
    attributes = None
    connection_by_handle = None
    _line = None

    def __init__(
        self,
        obj_id=None,
        obj_type=None,
        version=None,
        attributes=None,
        connections=None
    ):
        self.obj_id = obj_id
        self.obj_type = obj_type
        self.version = version
        self.attributes = attributes

        if not connections: connections = []

        self.connections_by_handle = {}
        for conn in connections:
            conn.obj = self
            self.connections_by_handle[conn.handle] = conn

        if self.is_line:
            self._line = LineComponent(self)

    def __repr__(self):
        return '<Object id="{}" type="{}" is_line={}>'.format(
            self.obj_id,
            self.obj_type,
            self.is_line
        )

    @property
    def connections(self):
        return list(self.connections_by_handle.values())

    @property
    def id(self):
        return self.obj_id

    @property
    def type(self):
        return self.obj_type

    @property
    def as_line(self):
        if not self.is_line:
            raise ValueError('object is not a line')
        return self._line

    @property
    def is_line(self):
        '''Returns true iff this object looks like a line. If true, the as_line 
        property will be accessible. if false, accessing as_line will throw
        an exception.'''

        return bool(
            self.attributes and (
                self.attributes.get('conn_endpoints') or
                self.attributes.get('orth_points') or
                self.attributes.get('bez_points') or
                self.attributes.get('poly_points')
            )
        )

    @property
    def connected_to(self):
        '''A list of connections from this object to other objects in the diagram. 
        The list contains Connection instance with the 'to' property pointing to
        other objects.'''

        return [
            obj.as_line.connection_to
            for obj in filter(
                lambda obj : obj.as_line.connected_from == self,
                self.diagram.objects.filter_lines()
            )
        ]

    @property
    def connected_to_objs(self):
        '''Similar to connected_to, but returns a list of Objects instead of Connections'''

        return [
            conn.to for conn in self.connected_to
        ]

    @property
    def outbound_lines(self):
        '''A list of lines connected to this object via their tails'''

        return [
            line_obj
            for line_obj in self.diagram.objects.filter_lines()
            if line_obj.as_line.connected_from == self
        ]

    @property
    def inbound_lines(self):
        '''A list of lines connected to this object via their heads'''

        return [
            line_obj
            for line_obj in self.diagram.objects.filter_lines()
            if line_obj.as_line.connected_to == self
        ]


class Connection:
    obj = None
    handle = None
    to_id = ''
    connection = 0

    def __init__(self, handle=None, to_id='', connection=0):
        assert handle != None and type(handle) == int
        self.handle = handle
        self.to_id = to_id
        self.connection = connection

    @property
    def to(self):
        '''The object instance pointed to by this connection'''

        return self.obj.diagram.objects[self.to_id]


def parse_connection(conn_node):
    return Connection(
        handle=int(conn_node.attrib['handle']),
        to_id=conn_node.attrib['to'],
        connection=conn_node.attrib['connection'],
    )


def parse_connections(obj_node):
    connections_node = obj_node.find(NS + 'connections')
    if not connections_node:
        return []

    return [
        parse_connection(conn_node)
        for conn_node in connections_node.findall(NS + 'connection')
    ]


def parse_object(obj_node):
    return Object(
        obj_id=obj_node.attrib['id'],
        obj_type=obj_node.attrib['type'],
        version=obj_node.attrib['version'],
        attributes=parse_attributes(obj_node),
        connections=parse_connections(obj_node),
    )

