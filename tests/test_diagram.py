
import site
site.addsitedir('src')

from dia_parser import Diagram, DiagramData, Layer, Group, Object, Connection

def test_create_empty_diagram():
    diagram = Diagram(
        DiagramData(),
        layers=[]
    )
    assert diagram

def test_create_diagram_with_layers():
    layer1 = Layer([])
    layer2 = Layer([])
    layer3 = Layer([])

    diagram = Diagram(
        DiagramData(),
        layers=[
            layer1,
            layer2,
            layer3,
        ]
    )
    assert diagram.layers == [layer1, layer2, layer3]

def test_it_assigns_diagram_to_layer():
    layer1 = Layer([])
    layer2 = Layer([])
    diagram = Diagram(
        DiagramData(),
        layers=[
            layer1,
            layer2,
        ]
    )

    assert layer1.diagram == diagram
    assert layer2.diagram == diagram

def test_diagram_find_object_returns_none_if_does_not_exist():
    obj = Object()
    diagram = Diagram(
        DiagramData(),
        layers=[]
    )
    assert diagram.find_object('123') == None

def test_diagram_find_object():
    obj = Object()
    obj.obj_id = '123'
    diagram = Diagram(
        DiagramData(),
        layers=[
            Layer([
                Group([
                    obj,
                ])
            ])
        ]
    )
    assert diagram.find_object('123') == obj

def test_diagram_iterates_layers():
    layer1 = Layer([])
    layer2 = Layer([])
    layer3 = Layer([])

    diagram = Diagram(
        DiagramData(),
        layers=[
            layer1,
            layer2,
            layer3,
        ]
    )
    assert list(diagram) == [layer1, layer2, layer3]
    
def test_diagram_iterates_over_lines():
    obj1 = Object(obj_id='1')
    obj2 = Object(obj_id='2')
    obj = Object(
        connections=(
            Connection(to_id=obj1.obj_id),
            Connection(to_id=obj2.obj_id),
        )
    )
    diagram = Diagram(
        DiagramData(),
        layers=[
            Layer([
                obj1,
                obj2,
                obj,
            ])
        ]
    )

    assert list(diagram.iter_line_objects()) == [obj]
