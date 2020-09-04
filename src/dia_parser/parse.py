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

import gzip
from xml.etree import ElementTree

from .ns import NS
from .diagram import parse_diagram

def read_gzip_file(src):
    return gzip.open(src).read()

def read_dia_file(src):
    '''Reads a .dia file (compressed or uncompressed) and returns the XML data as a string'''

    try:
        xml_data = read_gzip_file(src)
    except OSError:
        xml_data = open(src, 'rb').read()

    xml_data = xml_data.decode('utf-8')
    assert xml_data.lower().startswith('<?xml'), 'not a valid xml file'
    return xml_data

def parse_dia_file(src):
    xml_data = read_dia_file(src)

    root = ElementTree.fromstring(xml_data)
    assert root.tag == NS + 'diagram'

    return parse_diagram(root)
