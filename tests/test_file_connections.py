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
import os
import site
site.addsitedir('src')

from dia_parser import parse_dia_file

SRC = os.path.join('tests', 'data', 'connections.dia')

def test_it_can_load_file():
    assert parse_dia_file(SRC)

def test_it_loads_all_objects():
    diagram = parse_dia_file(SRC)
    assert len(list(diagram.objects)) == 22

def test_it_identifies_lines():
    diagram = parse_dia_file(SRC)
    assert len(list(diagram.objects.filter_lines())) == 11

def test_it_has_boxes():
    diagram = parse_dia_file(SRC)
    
    obj0 = diagram.objects['O0']
    assert not obj0.is_line
    assert obj0.type == 'Flowchart - Box'
    assert obj0.attributes['text']['string'] == '#Box has a line from its center#'

    obj1 = diagram.objects['O1']
    assert not obj1.is_line
    assert obj1.type == 'Flowchart - Box'
    assert obj1.attributes['text']['string'] == '#Box has a line to its center#'

    obj2 = diagram.objects['O2']
    assert obj2.is_line
    assert obj2.type == 'Standard - Line'
    assert obj2.connections[0].to_id == obj0.id
    assert obj2.connections[1].to_id == obj1.id

    obj3 = diagram.objects['O3']
    assert not obj3.is_line
    assert obj3.type == 'Flowchart - Box'
    assert obj3.attributes['text']['string'] == '#Box has text attached to it#'

    obj4 = diagram.objects['O4']
    assert not obj4.is_line
    assert obj4.type == 'Standard - Text'
    assert obj4.attributes['text']['string'] == '#Connected to a line#'
    assert obj4.connections[0].to_id == obj2.id

    obj5 = diagram.objects['O5']
    assert not obj5.is_line
    assert obj5.type == 'Standard - Text'
    assert obj5.attributes['text']['string'] == '#Connected to a box#'
    assert obj5.connections[0].to_id == obj3.id
