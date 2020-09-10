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

from xml.etree import ElementTree

import site
site.addsitedir('src')

from dia_parser import attributes

def parse_dia_element(doc_txt):
    '''Parses the given dia element, as a string, and returns the XML element'''

    data = '''<?xml version="1.0" encoding="UTF-8"?>
<wrapper xmlns:dia="http://www.lysator.liu.se/~alla/dia/">{}</wrapper>
'''.format(doc_txt)

    doc = ElementTree.fromstring(data)
    return doc[0]

def test_it_parses_real():
    el = parse_dia_element('<dia:real val="2.5399999618530273"/>')
    assert round(attributes.parse_real(el), 4) == 2.54

def test_it_parses_boolean_as_true():
    el = parse_dia_element('<dia:bool val="true"/>')
    assert attributes.parse_boolean(el)

def test_it_parses_boolean_as_false():
    el = parse_dia_element('<dia:bool val="false"/>')
    assert not attributes.parse_boolean(el)

def test_it_parses_point_as_tuple():
    el = parse_dia_element('<dia:point val="10.5,20.1"/>')
    assert attributes.parse_point(el) == (10.5, 20.1)

def test_it_parses_rectangle_as_tuple():
    el = parse_dia_element('<dia:rect val="1.5,2.5;3.5,4.5"/>')
    assert attributes.parse_rectangle(el) == (1.5, 2.5, 3.5, 4.5)

def test_it_parses_real():
    el = parse_dia_element('<dia:enum val="5"/>')
    assert attributes.parse_enum(el) == 5

def test_it_parses_enum():
    el = parse_dia_element('<dia:int val="3"/>')
    assert attributes.parse_int(el) == 3

def test_it_parses_string():
    el = parse_dia_element('<dia:string>#Hello world#</dia:string>')
    assert attributes.parse_string(el) == '#Hello world#'

def test_it_parses_color():
    el = parse_dia_element('<dia:color val="#12345678"/>')
    assert attributes.parse_color(el) == '#12345678'

def test_it_parses_a_list_of_attributes():
    data = '''
  <dia:composite type="grid">
    <dia:attribute name="dynamic">
      <dia:boolean val="true"/>
    </dia:attribute>
    <dia:attribute name="width_x">
      <dia:real val="1"/>
    </dia:attribute>
    <dia:attribute name="width_y">
      <dia:real val="1"/>
    </dia:attribute>
    <dia:attribute name="visible_x">
      <dia:int val="1"/>
    </dia:attribute>
    <dia:attribute name="visible_y">
      <dia:int val="1"/>
    </dia:attribute>
    <dia:composite type="color"/>
  </dia:composite>
    '''

    el = parse_dia_element(data)
    attrs = attributes.parse_attributes(el)
    assert attrs == {'dynamic': True, 'width_x': 1.0, 'width_y': 1.0, 'visible_x': 1, 'visible_y': 1}

