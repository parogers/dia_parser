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
from .obj import parse_object
from .attributes import parse_attributes

class Group:
    '''Represents a dia group node.'''

    attributes = None

    def __init__(self):
        self.objects = []
        self.groups = []

    def iter_line_objects(self):
        return filter(
            lambda obj : obj.is_line,
            self.iter_objects()
        )

    def iter_objects(self):
        yield from self.objects
        for group in self.groups:
            yield from group.iter_objects()


class Layer(Group):
    '''Represents a dia layer node.'''

    name = ''

    def __getitem__(self, obj_id):
        '''Returns an object matching the given object ID'''

        try:
            return next(filter(
                lambda obj : obj.obj_id == obj_id, self.objects
            ))
        except StopIteration:
            raise KeyError


def parse_layer(layer_node):
    '''Returns a Layer instance given a layer XML node'''

    layer = Layer()
    layer.name = layer_node.attrib['name']
    layer.visible = layer_node.attrib['visible'] == 'true'
    layer.connectable = layer_node.attrib['connectable'] == 'true'
    layer.active = layer_node.attrib['active'] == 'true'

    for obj_node in layer_node.findall(NS + 'object'):
        obj = parse_object(obj_node, layer)
        layer.objects.append(obj)

    for group_node in layer_node.findall(NS + 'group'):
        group = parse_group(group_node, layer)
        layer.groups.append(group)

    return layer


def parse_group(group_node, layer):
    '''Returns a Group instance given a group XML node'''

    group = Group()
    group.attributes = parse_attributes(group_node)

    for obj_node in group_node.findall(NS + 'object'):
        group.objects.append(
            parse_object(obj_node, layer)
        )

    for node in group_node.findall(NS + 'group'):
        group.groups.append(
            parse_group(node, layer)
        )

    return group
