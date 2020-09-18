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

SRC = os.path.join('tests', 'data', 'line-connections.dia')

def test_line_connects_from_box_to_nothing():
    diagram = parse_dia_file(SRC)

    obj = diagram.objects['O0']
    assert not obj.is_line

    line = diagram.objects['O1']
    assert line.is_line
    assert line.as_line.connected_from == obj

    assert not line.as_line.connected_to
