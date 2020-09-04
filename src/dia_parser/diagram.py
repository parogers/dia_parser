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


def parse_diagramdata(diagramdata_node):
    data = DiagramData()
    data.attributes = parse_attributes(diagramdata_node)
    return data


def parse_diagram(diagram_node):
    diagram = Diagram()

    node = diagram_node.find(NS + 'diagramdata')
    if node:
        diagram.diagram_data = parse_diagramdata(node)


    for layer_node in diagram_node.findall(NS + 'layer'):
        layer = parse_layer(layer_node)
        diagram.layers.append(layer)
    return diagram

