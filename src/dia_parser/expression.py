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

'''In this context an "expression" is a function that takes an DiaObject and yields back all derived objects (or values) that are considered to match the expression. For example:

```python
# This will yield back all objects connected to a given object, if the given object 
# looks like a line.
expr = expression.line_connected_to()

line_obj = diagram.objects['some-line-object']
for obj in expr(line_obj):
    print('line connects to:', obj)
```

The power of expressions is that they can be changed together. Most expression builders optionally takes an expression as an argument. Say you have a box and you want a list of all diamond shapes connected to it via lines:

```python
obj = diagram.objects['some-object']
expr = expression.outbound_lines(
    expression.line_connected_to(
        expression.has_type('Flowchart - Diamond')
    )
)

for diamond in expr(obj):
    print('object is connected to diamond:', diamond)
```

Note the object yielded back by each expression:

* expression.outbound_lines(expr) - Yields from expr(line), for each line pointing away from a given object
* expression.line_connected_to(expr) - Yields from expr(other), where other is the object pointed to by a given object (if it's a line)
* expression.has_type('Flowchart - Diamond') - Yields back objects that have type == 'Flowchart - Diamond'

Building on the example above, we could add a combiner expression to get the line objects and the diamonds they lead to:

```python
obj = diagram.objects['some-object']
expr = expression.outbound_lines(
    expression.combine(
        expression.line_connected_to(
            expression.has_type('Flowchart - Diamond')
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
    '''Creates an expression that matches outbound lines to the given expression. The new expression will yield back from the given expression applied to each line.'''

    def matches(obj):
        for line in obj.outbound_lines:
            yield from expr(line)

    return matches

def line_connected_to(expr=noop):
    '''Creates an expression that operates on the object pointed to by the given object, assuming given object is a line.'''

    def matches(obj):
        if obj.is_line:
            yield from expr(obj.as_line.connected_to)

    return matches

def connected_to_this(expr=noop):
    '''Creates an expression that operates on the list of objects connected to the given object'''

    def matches(obj):
        for other in obj.connected_to_this:
            yield from expr(other)

    return matches

def combine(expr=noop):
    '''Creates an expression that combines the given object, with the transformed (by sub-expression) object, and yields them back as tuples'''

    def matches(obj):
        for new_obj in expr(obj):
            yield (obj, new_obj)

    return matches

def has_type(type):
    '''Creates an expression that yields back the given object if it matches the given type'''

    def matches(obj):
        if obj.type == type:
            yield obj

    return matches

def has_text(text):
    '''Create an expression that matches on the given object text. The expression will yield back the object if matched.'''

    def matches(obj):
        if obj.text == text:
            yield obj

    return matches
