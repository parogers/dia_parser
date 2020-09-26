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

def noop(obj):
    yield obj

def outbound_lines(expr=noop):
    def matches(obj):
        for line in obj.outbound_lines:
            yield from expr(line)

    return matches

def line_connected_to(expr=noop):
    def matches(obj):
        if obj.is_line:
            yield from expr(obj.as_line.connected_to)

    return matches

def connected_to_this(expr):
    def matches(obj):
        for other in obj.connected_to_this:
            yield from expr(other)

    return matches

def combine(expr):
    def matches(obj):
        for new_obj in expr(obj):
            yield (obj, new_obj)

    return matches

def has_type(type):
    def matches(obj):
        if obj.type == type:
            yield obj

    return matches

def has_text(text):
    def matches(obj):
        if obj.text == text:
            yield obj

    return matches
