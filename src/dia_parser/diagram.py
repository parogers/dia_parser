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

from .attributes import parse_attributes
from .obj import parse_object
from .layer import parse_layer
from .ns import NS

class Diagram:
    layers = None
    object_map = None

    def __init__(self, diagram_data, layers):
        self.layers = list(layers)
        for layer in self.layers:
            layer.diagram = self
        self.object_map = {
            obj.obj_id : obj
            for obj in self.iter_objects()
        }

    def __iter__(self):
        '''Returns an iterator over the layers in this diagram'''

        return iter(self.layers)


    def __getitem__(self, name):
        '''Returns the layer matching the given name'''

        try:
            return next(filter(
                lambda layer : layer.name == name, self.layers
            ))
        except StopIteration:
            raise KeyError

    def iter_objects(self):
        '''Returns an iterator over all objects (Object) in this diagram'''

        for layer in self.layers:
            yield from layer.iter_objects()

    def iter_line_objects(self):
        return filter(
            lambda obj : hasattr(obj, 'is_line') and obj.is_line,
            self.iter_objects()
        )

    def find_object(self, obj_id):
        '''Returns an Object matching the given ID, or None'''

        return self.object_map.get(obj_id, None)

    @property
    def objects(self):
        '''The list of all objects in the diagram'''

        return list(self.iter_objects())


class DiagramData:
    attributes = None

    def __init__(self, attributes=None):
        if not attributes: attributes = {}
        self.attributes = attributes


def parse_diagramdata(diagramdata_node):
    return DiagramData(
        parse_attributes(diagramdata_node)
    )


def parse_diagram(diagram_node):
    node = diagram_node.find(NS + 'diagramdata')
    if node:
        diagram_data = parse_diagramdata(node)
    else:
        diagram_data = DiagramData({})

    layers = (
        parse_layer(node)
        for node in diagram_node.findall(NS + 'layer')
    )

    return Diagram(
        diagram_data,
        layers
    )

