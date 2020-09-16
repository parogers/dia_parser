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

import typing

from .ns import NS
from .obj import parse_object
from .attributes import parse_attributes

class GroupBase:
    def __init__(self, children):
        self.children = list(children)
        for node in self.children:
            node.parent = self

    def __iter__(self):
        '''Returns an iterator over all children'''

        return iter(self.children)

    def iter_objects(self):
        for child in self.children:
            if hasattr(child, 'children'):
                yield from child.iter_objects()
            else:
                yield child


class Group(GroupBase):
    '''Represents a dia group node.'''

    attributes = None
    parent = None

    def __init__(self, children, attributes=None):
        super().__init__(children)
        if not attributes: attributes = {}
        self.attributes = attributes


class Layer(GroupBase):
    '''Represents a dia layer node.'''

    name = ''
    diagram = None

    def __init__(self, children, name='', visible=False, connectable=False, active=False):
        super().__init__(children=children)
        self.name = name
        self.visible = visible
        self.connectable = connectable
        self.active = active

    @property
    def is_layer(self):
        return True


def parse_group_base(parent_node):
    '''Returns a tuple (Object list, Group list, Attribute dict) from the given top-level XML node'''

    children = []

    for node in parent_node.findall(NS + 'object'):
        children.append(
            parse_object(node)
        )

    for node in parent_node.findall(NS + 'group'):
        children.append(
            parse_group(node)
        )

    return (
        children,
        parse_attributes(parent_node),
    )


def parse_layer(layer_node):
    '''Returns a Layer instance given a layer XML node'''

    children, _ = parse_group_base(layer_node)

    return Layer(
        children=children,
        name=layer_node.attrib['name'],
        visible=(layer_node.attrib['visible'] == 'true'),
        connectable=(layer_node.attrib['connectable'] == 'true'),
        active=(layer_node.attrib.get('active', None) == 'true'),
    )


def parse_group(group_node):
    '''Returns a Group instance given a group XML node'''

    children, attributes = parse_group_base(group_node)

    return Group(
        children=children,
        attributes=attributes
    )
