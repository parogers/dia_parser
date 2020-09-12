
import site
site.addsitedir('src')

from dia_parser import Object, Diagram, DiagramData, Layer, Group, Connection

def test_object_diagram_property():
    obj = Object()
    diagram = Diagram(
        DiagramData(),
        layers=[
            Group([
                Group([
                    obj,
                ])
            ])
        ]
    )
    assert obj.diagram == diagram

def test_line_is_an_object_with_two_connections():
    obj1 = Object(obj_id='1')
    obj2 = Object(obj_id='2')
    obj = Object(
        connections=(
            Connection(to_id=obj1.obj_id),
            Connection(to_id=obj2.obj_id)
        )
    )
    assert obj.is_line

def test_default_object_is_not_a_line():
    assert not Object().is_line

def test_object_with_one_connection_is_not_a_line():
    obj1 = Object(obj_id='1')
    obj = Object(
        connections=(
            Connection(to_id=obj1.obj_id),
        )
    )
    assert not obj.is_line
