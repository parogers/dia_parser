
import site
site.addsitedir('src')

from dia_parser import Diagram, DiagramData, Layer

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
