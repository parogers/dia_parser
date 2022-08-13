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

'''In this context an "expression" is a generator function that takes an 
DiaObject and iterates over all derived values matching the expression.
For example:

```python
# This will yield back all objects connected to a given line object
expr = line_connected_to()

line_obj = diagram.objects['some-line-object']
for obj in expr(line_obj):
    print('line_obj points to:', obj)
```

Which alone isn't very useful because it iterates over at most one object. But
expressions can be commposed to do more interesting things. Say you have an
object and you want a list of all diamond shapes connected to it via lines:

```python
expr = outbound_lines(
    line_connected_to(
        has_type('Flowchart - Diamond')
    )
)

obj = diagram.objects['some-object']
for diamond in expr(obj):
    print('object is connected to diamond:', diamond)
```

How it works:

* outbound_lines - iterates over each outbound line, and yields from expr(line)
* line_connected_to - if the object is a line, yields back expr(line)
* has_type - if the object is of a type, yield it back

Building on the example above, we could add a combiner expression to get the 
line objects and the diamonds they lead to:

```python
obj = diagram.objects['some-object']
expr = outbound_lines(
    combine(
        line_connected_to(
            has_type('Flowchart - Diamond')
        )
    )
)

for line, diamond in expr(obj):
    print('object is connected to diamond via line:', line, diamond)
```

'''

def noop(obj):
    '''Yields back the object given'''

    yield obj

def outbound_lines(expr=noop):
    '''Creates an expression iterates over the outbound lines of an object,
    then yields back from expr(line)'''

    def matches(obj):
        for line in obj.outbound_lines:
            yield from expr(line)

    return matches

def inbound_lines(expr=noop):
    '''Creates an expression iterates over the inbound lines of an object,
    then yields back from expr(line)'''

    def matches(obj):
        for line in obj.inbound_lines:
            yield from expr(line)

    return matches

def line_connected_to(expr=noop):
    '''Creates an expression that, given a line object, yields from expr(to)
    where 'to' is the object the line connects to.'''

    def matches(obj):
        if obj.is_line:
            yield from expr(obj.as_line.connected_to)

    return matches

def line_connected_from(expr=noop):
    '''Creates an expression that, given a line object, yields from expr(from)
    where 'from' is the object the line connects from.'''

    def matches(obj):
        if obj.is_line:
            yield from expr(obj.as_line.connected_from)

    return matches

def connected_to_this(expr=noop):
    '''Creates an expression that operates on the list of objects connected to 
    the given object'''

    def matches(obj):
        for other in obj.connected_to_this:
            yield from expr(other)

    return matches

def combine(expr=noop):
    '''Creates an expression that combines the given object, with the 
    transformed (by sub-expression) object, and yields them back as tuples'''

    def matches(obj):
        for new_obj in expr(obj):
            yield (obj, new_obj)

    return matches

def has_type(type):
    '''Creates an expression that yields back the given object if it matches the
    given type'''

    def matches(obj):
        if obj.type == type:
            yield obj

    return matches

def has_text(text):
    '''Create an expression that matches on the given object text. The 
    expression will yield back the object if matched.'''

    def matches(obj):
        if obj.text == text:
            yield obj

    return matches

def first(expr):
    '''Creates an expression that yields back the first object in expr(obj)'''

    def matches(obj):
        try:
            yield next(expr(obj))
        except StopIteration:
            yield None

    return matches

def all(expr):
    '''Creates an expression that iterates object an object list, and yields
    back from expr(obj)'''

    def matches(obj_list):
        for obj in obj_list:
            yield from expr(obj)

    return matches
