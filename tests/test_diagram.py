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

import pytest
import site
site.addsitedir('src')

from dia_parser import Diagram, DiagramData, Layer, Group, Object, Connection

def test_create_empty_diagram():
    diagram = Diagram(
        [],
        DiagramData(),
    )
    assert diagram

def test_create_diagram_with_layers():
    layer1 = Layer([])
    layer2 = Layer([])
    layer3 = Layer([])

    diagram = Diagram(
        [
            layer1,
            layer2,
            layer3,
        ],
        DiagramData(),
    )
    assert diagram.layers == [layer1, layer2, layer3]

def test_it_assigns_diagram_to_layer():
    layer1 = Layer([])
    layer2 = Layer([])
    diagram = Diagram(
        [
            layer1,
            layer2,
        ],
        DiagramData(),
    )

    assert layer1.diagram == diagram
    assert layer2.diagram == diagram

def test_lookup_object_by_id_raises_keyerror():
    obj = Object()
    diagram = Diagram(
        [],
        DiagramData(),
    )
    with pytest.raises(KeyError):
        assert diagram.objects['123']

def test_lookup_object_by_id():
    obj = Object()
    obj.obj_id = '123'
    diagram = Diagram(
        [
            Layer([
                Group([
                    obj,
                ])
            ])
        ],
        DiagramData(),
    )
    assert diagram.objects['123'] == obj

def test_diagram_iterates_layers():
    layer1 = Layer([])
    layer2 = Layer([])
    layer3 = Layer([])

    diagram = Diagram(
        [
            layer1,
            layer2,
            layer3,
        ],
        DiagramData(),
    )
    assert list(diagram) == [layer1, layer2, layer3]

def test_diagram_iterates_over_lines():
    obj1 = Object(obj_id='1')
    obj2 = Object(obj_id='2')
    obj = Object(
        attributes={
            'conn_endpoints' : [
                (0, 0),
                (1, 1),
            ]
        },
        connections=(
            Connection(handle=0, to_id=obj1.obj_id),
            Connection(handle=1, to_id=obj2.obj_id),
        )
    )
    diagram = Diagram(
        [
            Layer([
                obj1,
                obj2,
                obj,
            ])
        ],
        DiagramData(),
    )

    assert list(diagram.objects.filter_lines()) == [obj]

def test_lookup_layer_by_name():
    diagram = Diagram(
        [
            Layer([
            ])
        ],
        DiagramData(),
    )

def test_diagram_iterates_over_objects():
    obj1 = Object(obj_id='1')
    obj2 = Object(obj_id='2')
    obj = Object(
        connections=(
            Connection(handle=0, to_id=obj1.obj_id),
            Connection(handle=1, to_id=obj2.obj_id),
        )
    )
    diagram = Diagram(
        [
            Layer([
                obj1,
                obj2,
                obj,
            ])
        ],
        DiagramData(),
    )

    assert list(diagram.objects) == [obj1, obj2, obj]

def test_diagram_iterates_over_nodes():
    obj1 = Object(obj_id='1')
    obj2 = Object(obj_id='2')
    obj = Object(
        connections=(
            Connection(handle=0, to_id=obj1.obj_id),
            Connection(handle=1, to_id=obj2.obj_id),
        )
    )
    group = Group([
        obj1,
        obj2,
    ])
    diagram = Diagram(
        [
            Layer([
                group,
                obj,
            ])
        ],
        DiagramData(),
    )

    assert list(diagram.nodes) == [group, obj1, obj2, obj]
