
import site
site.addsitedir('src')

from dia_parser import Object, Diagram, DiagramData, Layer, Group

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

