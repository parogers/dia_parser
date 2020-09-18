#!/usr/bin/env python3

from dia_parser import parse_dia_file

diagram = parse_dia_file('Diagram1.dia')

# Iterate over all layers in the diagram
for layer in diagram:
    pass

# Lookup a layer by name
layer = diagram['Background']

# Iterate over direct children of layer
for child in layer:
    pass

# Lookup an object by ID
obj = diagram.objects['O5']

# Iterate over all objects in the diagram
for obj in diagram.objects:
    pass

# Iterate over all nodes (objects and groups) in a diagram
for node in diagram.nodes:
    pass

# List of line objects pointing away from the given obj
lines = obj.outbound_lines

# List of line objects pointing at the given obj
lines = obj.inbound_lines

# List of (line, obj) tuples pointing away from obj
for line, other in obj.outbound:
    pass

# List of (line, obj) tuples pointing at obj
for line, other in obj.inbound:
    pass

# List of objects connected to the given object (ie the objects
# that have a connection pointing to the given object)
objs = obj.connected_to_this

