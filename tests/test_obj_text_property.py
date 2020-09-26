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

from dia_parser import Object

def test_object_text_property_returns_the_attribute():
    obj = Object(
        obj_id='123',
        obj_type='Testing',
        attributes={
            'text' : {
                'string' : '#hello world#',
            },
        },
    )
    assert obj.text == 'hello world'

def test_object_text_property_returns_none_if_text_attribute_missing():
    obj = Object(
        obj_id='123',
        obj_type='Testing',
        attributes={
        },
    )
    assert obj.text == None

def test_object_text_property_returns_none_if_string_attribute_missing():
    obj = Object(
        obj_id='123',
        obj_type='Testing',
        attributes={
            'text' : {
            },
        },
    )
    assert obj.text == None

def test_object_text_property_works_without_pound_signs():
    obj = Object(
        obj_id='123',
        obj_type='Testing',
        attributes={
            'text' : {
                'string' : 'hello world',
            },
        },
    )
    assert obj.text == 'hello world'
