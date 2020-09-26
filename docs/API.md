# Table of Contents

* [dia\_parser/parse](#dia_parser/parse)
  * [read\_dia\_file](#dia_parser/parse.read_dia_file)
* [dia\_parser/diagram](#dia_parser/diagram)
  * [ObjectsComponent](#dia_parser/diagram.ObjectsComponent)
    * [\_\_iter\_\_](#dia_parser/diagram.ObjectsComponent.__iter__)
    * [\_\_getitem\_\_](#dia_parser/diagram.ObjectsComponent.__getitem__)
    * [filter\_lines](#dia_parser/diagram.ObjectsComponent.filter_lines)
  * [Diagram](#dia_parser/diagram.Diagram)
    * [\_\_iter\_\_](#dia_parser/diagram.Diagram.__iter__)
    * [\_\_getitem\_\_](#dia_parser/diagram.Diagram.__getitem__)
    * [nodes](#dia_parser/diagram.Diagram.nodes)
  * [parse\_diagram](#dia_parser/diagram.parse_diagram)
* [dia\_parser/obj](#dia_parser/obj)
  * [LineComponent](#dia_parser/obj.LineComponent)
    * [connection\_to](#dia_parser/obj.LineComponent.connection_to)
    * [connection\_from](#dia_parser/obj.LineComponent.connection_from)
    * [connected\_to](#dia_parser/obj.LineComponent.connected_to)
    * [connected\_from](#dia_parser/obj.LineComponent.connected_from)
  * [Node](#dia_parser/obj.Node)
    * [layer](#dia_parser/obj.Node.layer)
    * [diagram](#dia_parser/obj.Node.diagram)
  * [Object](#dia_parser/obj.Object)
    * [text](#dia_parser/obj.Object.text)
    * [as\_line](#dia_parser/obj.Object.as_line)
    * [is\_line](#dia_parser/obj.Object.is_line)
    * [outbound\_lines](#dia_parser/obj.Object.outbound_lines)
    * [inbound\_lines](#dia_parser/obj.Object.inbound_lines)
    * [outbound](#dia_parser/obj.Object.outbound)
    * [inbound](#dia_parser/obj.Object.inbound)
    * [connected\_to\_this](#dia_parser/obj.Object.connected_to_this)
  * [Connection](#dia_parser/obj.Connection)
    * [to](#dia_parser/obj.Connection.to)
* [dia\_parser/layer](#dia_parser/layer)
  * [GroupBase](#dia_parser/layer.GroupBase)
    * [\_\_iter\_\_](#dia_parser/layer.GroupBase.__iter__)
    * [iter\_nodes](#dia_parser/layer.GroupBase.iter_nodes)
  * [Group](#dia_parser/layer.Group)
  * [Layer](#dia_parser/layer.Layer)
  * [parse\_group\_base](#dia_parser/layer.parse_group_base)
  * [parse\_layer](#dia_parser/layer.parse_layer)
  * [parse\_group](#dia_parser/layer.parse_group)
* [dia\_parser/attributes](#dia_parser/attributes)
  * [parse\_attributes](#dia_parser/attributes.parse_attributes)

<a name="dia_parser/parse"></a>
# dia\_parser/parse

<a name="dia_parser/parse.read_dia_file"></a>
#### read\_dia\_file

```python
read_dia_file(src)
```

Reads a .dia file (compressed or uncompressed) and returns the XML data as a string

<a name="dia_parser/diagram"></a>
# dia\_parser/diagram

<a name="dia_parser/diagram.ObjectsComponent"></a>
## ObjectsComponent

```python
class ObjectsComponent()
```

Used to lookup objects by ID in a diagram, or list them

<a name="dia_parser/diagram.ObjectsComponent.__iter__"></a>
#### \_\_iter\_\_

```python
 | __iter__()
```

Iterates over all objects in the diagram

<a name="dia_parser/diagram.ObjectsComponent.__getitem__"></a>
#### \_\_getitem\_\_

```python
 | __getitem__(obj_name)
```

Lookup an object given the ID

<a name="dia_parser/diagram.ObjectsComponent.filter_lines"></a>
#### filter\_lines

```python
 | filter_lines()
```

Returns an iterator over all line type objects in the diagram

<a name="dia_parser/diagram.Diagram"></a>
## Diagram

```python
class Diagram()
```

Represents a dia diagram node.

**Attributes**:

- `layers` - list of Layer instances
- `objects` - an ObjectsComponent instance used to access objects in the diagram

<a name="dia_parser/diagram.Diagram.__iter__"></a>
#### \_\_iter\_\_

```python
 | __iter__()
```

Returns an iterator over the layers in this diagram

<a name="dia_parser/diagram.Diagram.__getitem__"></a>
#### \_\_getitem\_\_

```python
 | __getitem__(name)
```

Returns the layer matching the given name

<a name="dia_parser/diagram.Diagram.nodes"></a>
#### nodes

```python
 | @property
 | nodes()
```

An iterator over all nodes (objects and groups) in this diagram

<a name="dia_parser/diagram.parse_diagram"></a>
#### parse\_diagram

```python
parse_diagram(diagram_node)
```

Return a Diagram instance given an XML node

<a name="dia_parser/obj"></a>
# dia\_parser/obj

<a name="dia_parser/obj.LineComponent"></a>
## LineComponent

```python
class LineComponent()
```

Provides methods for interpreting/treating a dia object as a line

<a name="dia_parser/obj.LineComponent.connection_to"></a>
#### connection\_to

```python
 | @property
 | connection_to()
```

The connection representing the head of this line object (throws AssertionError if not a line)

<a name="dia_parser/obj.LineComponent.connection_from"></a>
#### connection\_from

```python
 | @property
 | connection_from()
```

The connection representing the tail of this line object (throws AssertionError if not a line)

<a name="dia_parser/obj.LineComponent.connected_to"></a>
#### connected\_to

```python
 | @property
 | connected_to()
```

The object pointed to by the head of this line (throws AssertionError if not a line)

<a name="dia_parser/obj.LineComponent.connected_from"></a>
#### connected\_from

```python
 | @property
 | connected_from()
```

The object pointed to by the tail of this line (throws AssertionError if not a line)

<a name="dia_parser/obj.Node"></a>
## Node

```python
class Node()
```

A node is the common base class to a dia object, and a dia group

<a name="dia_parser/obj.Node.layer"></a>
#### layer

```python
 | @property
 | layer()
```

The layer containing this object

<a name="dia_parser/obj.Node.diagram"></a>
#### diagram

```python
 | @property
 | diagram()
```

The diagram containing this object

<a name="dia_parser/obj.Object"></a>
## Object

```python
class Object(Node)
```

Represents a dia object node.

**Attributes**:

- `id` - the object ID (unique across the diagram)
- `type` - a string describing the type (eg "Flowchart - Box")
- `version` - the version
- `attributes` - a dictionary of attributes on the object
- `parent` - the parent to this object (ie Layer or Group instance)

<a name="dia_parser/obj.Object.text"></a>
#### text

```python
 | @property
 | text()
```

Returns the text/string attribute of this object, or None if missing.
Note dia text strings are stored with a leading and trailing '#' character. 
This property returns the string with those characters removed.

<a name="dia_parser/obj.Object.as_line"></a>
#### as\_line

```python
 | @property
 | as_line()
```

The LineComponent instance for this object, if it reads as a line type object. (ie is_line=True)

<a name="dia_parser/obj.Object.is_line"></a>
#### is\_line

```python
 | @property
 | is_line()
```

Returns true iff this object looks like a line. If true, the as_line
property will be accessible. if false, accessing as_line will throw
an exception.

<a name="dia_parser/obj.Object.outbound_lines"></a>
#### outbound\_lines

```python
 | @property
 | outbound_lines()
```

A list of lines connected to this object via their tails

<a name="dia_parser/obj.Object.inbound_lines"></a>
#### inbound\_lines

```python
 | @property
 | inbound_lines()
```

A list of lines connected to this object via their heads

<a name="dia_parser/obj.Object.outbound"></a>
#### outbound

```python
 | @property
 | outbound()
```

A list of (line, to_obj) tuples where line connects from this object to to_obj

<a name="dia_parser/obj.Object.inbound"></a>
#### inbound

```python
 | @property
 | inbound()
```

A list of (line, from_obj) tuples where line connects from from_obj to this object

<a name="dia_parser/obj.Object.connected_to_this"></a>
#### connected\_to\_this

```python
 | @property
 | connected_to_this()
```

The list of objects connected to this object

<a name="dia_parser/obj.Connection"></a>
## Connection

```python
class Connection()
```

Represents a dia connection node.

**Attributes**:

- `obj` - the (source) object to which this connection belongs
- `handle` - the handle number of of this connection, used to identify where on the source object the connection is
- `to_id` - the (target) object ID to which this connection is attached
- `connection` - the connection point (number) on the attached object

<a name="dia_parser/obj.Connection.to"></a>
#### to

```python
 | @property
 | to()
```

The object instance pointed to by this connection

<a name="dia_parser/layer"></a>
# dia\_parser/layer

<a name="dia_parser/layer.GroupBase"></a>
## GroupBase

```python
class GroupBase()
```

<a name="dia_parser/layer.GroupBase.__iter__"></a>
#### \_\_iter\_\_

```python
 | __iter__()
```

Returns an iterator over all children

<a name="dia_parser/layer.GroupBase.iter_nodes"></a>
#### iter\_nodes

```python
 | iter_nodes()
```

Returns an iterator over all nodes (objects and groups)

<a name="dia_parser/layer.Group"></a>
## Group

```python
class Group(GroupBase,  Node)
```

Represents a dia group node.

<a name="dia_parser/layer.Layer"></a>
## Layer

```python
class Layer(GroupBase)
```

Represents a dia layer node.

<a name="dia_parser/layer.parse_group_base"></a>
#### parse\_group\_base

```python
parse_group_base(parent_node)
```

Returns a tuple (Object list, Group list, Attribute dict) from the given top-level XML node

<a name="dia_parser/layer.parse_layer"></a>
#### parse\_layer

```python
parse_layer(layer_node)
```

Returns a Layer instance given a layer XML node

<a name="dia_parser/layer.parse_group"></a>
#### parse\_group

```python
parse_group(group_node)
```

Returns a Group instance given a group XML node

<a name="dia_parser/attributes"></a>
# dia\_parser/attributes

<a name="dia_parser/attributes.parse_attributes"></a>
#### parse\_attributes

```python
parse_attributes(parent_node)
```

Return a dictionary representing the attributes/values found under the given dia XML node

