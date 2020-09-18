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

SRC = os.path.join('tests', 'data', 'lines.dia')

def test_all_lines_connect_two_boxes():
    diagram = parse_dia_file(SRC)

    box1 = diagram.objects['O0']
    box2 = diagram.objects['O1']

    for line in diagram.objects.filter_lines():
        assert line.as_line.connected_from == box1
        assert line.as_line.connected_to == box2
    

def test_connection_handles_for_basic_line():
    diagram = parse_dia_file(SRC)

    box1 = diagram.objects['O0']
    box2 = diagram.objects['O1']

    line = diagram.objects['O2']
    assert line.type == 'Standard - Line'
    assert line.is_line
    assert line.as_line.connection_from.handle == 0
    assert line.as_line.connection_to.handle == 1

    assert line.as_line.connected_from == box1
    assert line.as_line.connected_to == box2
