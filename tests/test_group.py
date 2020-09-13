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

import site
site.addsitedir('src')

from dia_parser import Group, Object, Layer

def test_group_iterates_all_objects():
    obj1 = Object()
    obj2 = Object()
    obj3 = Object()
    group = Group([
        obj1,
        obj2,
        Group([
            obj3,
        ])
    ])

    assert list(group.iter_objects()) == [obj1, obj2, obj3]

def test_it_assigns_the_parent_node():
    obj1 = Object()
    obj2 = Object()
    obj3 = Object()
    group2 = Group([
        obj3,
    ])
    group1 = Group([
        obj1,
        obj2,
        group2,
    ])

    assert obj1.parent == group1
    assert obj2.parent == group1
    assert group2.parent == group1
    assert obj3.parent == group2
