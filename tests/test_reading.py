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

import tempfile
import pytest
import os
import site
site.addsitedir('src')

from dia_parser import read_dia_file, parse_dia_file, Diagram

def test_it_reads_a_compressed_dia_file():
    data = read_dia_file(
        os.path.join('tests', 'data', 'empty.dia')
    )
    assert data.startswith('<?xml version="1.0" encoding="UTF-8"?>\n<dia:diagram xmlns:dia="http://www.lysator.liu.se/~alla/dia/">')

def test_it_reads_an_uncompressed_dia_file():
    data = read_dia_file(
        os.path.join('tests', 'data', 'empty-uncompressed.dia')
    )
    assert data.startswith('<?xml version="1.0" encoding="UTF-8"?>\n<dia:diagram xmlns:dia="http://www.lysator.liu.se/~alla/dia/">')

def test_it_raises_an_assertion_error_if_file_is_invalid():
    with tempfile.NamedTemporaryFile() as tmp:
        open(tmp.name, 'w').write('Hello world')
        with pytest.raises(AssertionError):
            read_dia_file(tmp.name)

def test_it_parses_a_dia_file_and_returns_diagram_instance():
    diagram = parse_dia_file(
        os.path.join('tests', 'data', 'Diagram1.dia')
    )
    assert isinstance(diagram, Diagram)

def test_it_parses_a_dia_file_and_reads_layers():
    diagram = parse_dia_file(
        os.path.join('tests', 'data', 'Diagram1.dia')
    )

    assert len(diagram.layers) == 2
    assert diagram.layers[0].name == 'Background'
    assert diagram.layers[1].name == 'Second'

def test_it_parses_and_iterates_over_all_objects():
    diagram = parse_dia_file(
        os.path.join('tests', 'data', 'Diagram1.dia')
    )

    id_list = [obj.obj_id for obj in diagram.layers[0].iter_objects()]
    assert id_list == ['O0', 'O1', 'O2', 'O3', 'O4', 'O5', 'O6', 'O7', 'O8', 'O9', 'O10', 'O11']
