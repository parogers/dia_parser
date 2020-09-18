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

from dia_parser import Object, Diagram, DiagramData, Layer, Group, Connection

def test_object_diagram_property():
    obj = Object()
    diagram = Diagram(
        DiagramData(),
        layers=[
            Layer([
                Group([
                    obj,
                ])
            ])
        ]
    )
    assert obj.diagram == diagram

def test_line_is_an_object_with_two_connections():
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
            Connection(handle=1, to_id=obj2.obj_id)
        )
    )
    assert obj.is_line

def test_default_object_is_not_a_line():
    assert not Object().is_line

def test_connection_points_to_object():
    obj1 = Object(obj_id='1')
    obj2 = Object(
        connections=(
            Connection(handle=0, to_id=obj1.obj_id),
        )
    )
    diagram = Diagram(
        DiagramData(),
        layers=[
            Layer([
                obj1,
                obj2,
            ])
        ]
    )
    
    assert obj2.connections[0].to == obj1

def test_object_has_line_sub_component():
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
        DiagramData(),
        layers=[
            Layer([
                obj1,
                obj2,
                obj,
            ])
        ]
    )

    assert obj.as_line


def test_non_line_object_raises_exception_as_line():
    obj = Object(obj_id='1')
    diagram = Diagram(
        DiagramData(),
        layers=[
            Layer([
                obj,
            ])
        ]
    )

    with pytest.raises(ValueError):
        obj.as_line


def test_line_has_connections_to_from_objects():
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
        DiagramData(),
        layers=[
            Layer([
                obj1,
                obj2,
                obj,
            ])
        ]
    )

    assert obj.as_line.connection_from.to == obj1
    assert obj.as_line.connection_to.to == obj2

    assert obj.as_line.connected_from == obj1
    assert obj.as_line.connected_to == obj2

def test_object_connects_to_other_objects_via_connections():
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
        DiagramData(),
        layers=[
            Layer([
                obj1,
                obj2,
                obj,
            ])
        ]
    )

    assert obj1.connected_to == [obj.connections[1]]

def test_object_connects_to_other_objects():
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
        DiagramData(),
        layers=[
            Layer([
                obj1,
                obj2,
                obj,
            ])
        ]
    )

    assert obj1.connected_to_objs == [obj2]

def test_object_diagram_property():
    obj = Object()
    layer = Layer([
        Group([
            obj,
        ])
    ])
    diagram = Diagram(
        DiagramData(),
        layers=[
            layer,
        ]
    )
    assert obj.layer == layer
