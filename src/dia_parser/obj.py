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
    def connections(self):
        return self.obj.connections

    @property
    def connection_to(self):
        '''The connection representing the head of this line object (throws AssertionError if not a line)'''

        return self.connections[1]

    @property
    def connection_from(self):
        '''The connection representing the tail of this line object (throws AssertionError if not a line)'''

        return self.connections[0]

    @property
    def connected_to(self):
        '''The object pointed to by the head of this line (throws AssertionError if not a line)'''

        return self.connection_to.to

    @property
    def connected_from(self):
        '''The object pointed to by the tail of this line (throws AssertionError if not a line)'''

        return self.connection_from.to



class Object:
    obj_id = ''
    obj_type = ''
    version = ''
    attributes = None
    connections = None
    parent = None
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

        self.connections = list(connections)
        for conn in self.connections:
            conn.obj = self

        if self.is_line:
            self._line = LineComponent(self)

    def __repr__(self):
        return '<Object id="{}" type="{}" version="{}">'.format(
            self.obj_id,
            self.obj_type,
            self.version
        )

    @property
    def as_line(self):
        if not self.is_line:
            raise ValueError('object is not a line')
        return self._line

    @property
    def diagram(self):
        node = self.parent
        while node:
            if hasattr(node, 'diagram'):
                return node.diagram
            if not hasattr(node, 'parent'):
                break
            node = node.parent
        return None

    @property
    def is_line(self):
        return self.connections and len(self.connections) == 2

    @property
    def connected_to(self):
        '''A list of connections from this object to other objects in the diagram. 
        The list contains Connection instance with the 'to' property pointing to
        other objects.'''

        return [
            obj.as_line.connection_to
            for obj in filter(
                lambda obj : obj.as_line.connected_from == self,
                self.diagram.iter_line_objects()
            )
        ]

    @property
    def connected_to_objs(self):
        '''Similar to connected_to, but returns a list of Objects instead of Connections'''

        return [
            conn.to for conn in self.connected_to
        ]


class Connection:
    obj = None
    handle = ''
    to_id = ''
    connection = 0

    def __init__(self, handle='', to_id='', connection=0):
        self.handle = handle
        self.to_id = to_id
        self.connection = connection

    @property
    def to(self):
        '''The object instance pointed to by this connection'''

        return self.obj.diagram.objects[self.to_id]


def parse_connection(conn_node):
    return Connection(
        handle=conn_node.attrib['handle'],
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

