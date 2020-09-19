# Table of Contents

* [dia\_parser/diagram](#dia_parser/diagram)
  * [Diagram](#dia_parser/diagram.Diagram)
    * [\_\_iter\_\_](#dia_parser/diagram.Diagram.__iter__)
    * [\_\_getitem\_\_](#dia_parser/diagram.Diagram.__getitem__)
    * [nodes](#dia_parser/diagram.Diagram.nodes)
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
    * [is\_line](#dia_parser/obj.Object.is_line)
    * [outbound\_lines](#dia_parser/obj.Object.outbound_lines)
    * [inbound\_lines](#dia_parser/obj.Object.inbound_lines)
    * [outbound](#dia_parser/obj.Object.outbound)
    * [inbound](#dia_parser/obj.Object.inbound)
    * [connected\_to\_this](#dia_parser/obj.Object.connected_to_this)
  * [Connection](#dia_parser/obj.Connection)
    * [to](#dia_parser/obj.Connection.to)

<a name="dia_parser/diagram"></a>
# dia\_parser/diagram

<a name="dia_parser/diagram.Diagram"></a>
## Diagram

```python
class Diagram()
```

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

<a name="dia_parser/obj"></a>
# dia\_parser/obj

<a name="dia_parser/obj.LineComponent"></a>
## LineComponent

```python
class LineComponent()
```

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

<a name="dia_parser/obj.Connection.to"></a>
#### to

```python
 | @property
 | to()
```

The object instance pointed to by this connection

