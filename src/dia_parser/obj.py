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


class Object:
    obj_id = ''
    obj_type = ''
    version = ''
    attributes = None
    connections = None
    parent = None

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
        self.connections = connections

    def __repr__(self):
        return '<Object id="{}" type="{}" version="{}">'.format(
            self.obj_id,
            self.obj_type,
            self.version
        )

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

    @property
    def to(self):
        return self.layer[self.to_id]


def parse_connection(conn_node):
    conn = Connection()
    conn.handle = conn_node.attrib['handle']
    conn.to_id = conn_node.attrib['to']
    conn.connection = conn_node.attrib['connection']
    return conn


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

