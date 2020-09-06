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

def parse_real(value_node):
    return float(value_node.attrib['val'])

def parse_boolean(value_node):
    return bool(value_node.attrib['val'])

def parse_point(value_node):
    args = value_node.attrib['val'].split(',')
    return (
        float(args[0]),
        float(args[1]),
    )

def parse_rectangle(value_node):
    left, right = value_node.attrib['val'].split(';')
    args1 = left.split(',')
    args2 = right.split(',')
    return (
        float(args1[0]),
        float(args1[1]),
        float(args2[0]),
        float(args2[1]),
    )

def parse_enum(value_node):
    return int(value_node.attrib['val'])

def parse_int(value_node):
    return int(value_node.attrib['val'])

def parse_string(value_node):
    return value_node.text

def parse_color(value_node):
    return value_node.attrib['val']

def parse_font(value_node):
    return (
        value_node.attrib['family'],
        value_node.attrib['style'],
        value_node.attrib['name']
    )

def parse_attribute_value(attrib_node):
    if len(attrib_node) == 0:
        return None

    value_node = list(attrib_node)[0]

    tag = value_node.tag[len(NS):]
    if tag == 'real':
        return parse_real(value_node)
    elif tag == 'boolean':
        return parse_boolean(value_node)
    elif tag == 'point':
        return parse_point(value_node)
    elif tag == 'rectangle':
        return parse_rectangle(value_node)
    elif tag == 'enum':
        return parse_enum(value_node)
    elif tag == 'composite':
        return parse_attributes(value_node)
    elif tag == 'string':
        return parse_string(value_node)
    elif tag == 'color':
        return parse_color(value_node)
    elif tag == 'font':
        return parse_font(value_node)
    elif tag == 'int':
        return parse_int(value_node)

    print('unknown tag', tag)

    return ''

def parse_attributes(parent_node):
    attributes = {}

    for attrib_node in parent_node.findall(NS + 'attribute'):
        name = attrib_node.attrib['name']
        try:
            avalue = parse_attribute_value(attrib_node)
        except Exception as ex:
            print('error parsing attribute value for', name, ':', ex)
            raise

        attributes[name] = avalue

    return attributes

