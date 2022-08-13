
import site
site.addsitedir('src')

from dia_parser import expression, Layer, Object, Connection, Diagram


def make_straight_line(obj1, obj2):
    line = Object(
        attributes={
            'conn_endpoints' : [
                (0, 0),
                (1, 1),
            ]
        },
        connections=(
            Connection(handle=0, to_id=obj1.obj_id),
            Connection(handle=1, to_id=obj2.obj_id)
        )
    )
    return line


def test_it_iters_over_outbound_lines():
    obj1 = Object(obj_id='1')
    obj2 = Object(obj_id='2')
    obj3 = Object(obj_id='3')
    obj4 = Object(obj_id='4')
    obj5 = Object(obj_id='5')
    line1 = make_straight_line(obj1, obj2)
    line2 = make_straight_line(obj1, obj3)
    line3 = make_straight_line(obj1, obj4)
    line4 = make_straight_line(obj1, obj5)
    layer = Layer([
        obj1,
        obj2,
        obj3,
        obj4,
        obj5,
        line1,
        line2,
        line3,
        line4,
    ])
    diagram = Diagram([layer])
    lines = expression.outbound_lines()(obj1)
    assert set(lines) == set([line1, line2, line3, line4])


def test_it_iters_over_line_connected_to():
    obj1 = Object(obj_id='1')
    obj2 = Object(obj_id='2')
    line = make_straight_line(obj1, obj2)
    layer = Layer([
        obj1,
        obj2,
        line,
    ])
    diagram = Diagram([layer])
    objects = expression.line_connected_to()(line)
    assert set(objects) == set([obj2])


def test_it_iters_over_lines_connected_to_this():
    obj1 = Object(obj_id='1')
    obj2 = Object(obj_id='2')
    obj3 = Object(obj_id='3')
    obj4 = Object(obj_id='4')
    obj5 = Object(obj_id='5')
    line1 = make_straight_line(obj2, obj1)
    line2 = make_straight_line(obj3, obj1)
    line3 = make_straight_line(obj4, obj1)
    line4 = make_straight_line(obj5, obj1)
    layer = Layer([
        obj1,
        obj2,
        obj3,
        obj4,
        obj5,
        line1,
        line2,
        line3,
        line4,
    ])
    diagram = Diagram([layer])
    lines = expression.connected_to_this()(obj1)
    assert set(lines) == set([line1, line2, line3, line4])

    lines2 = expression.connected_to_this()(obj5)
    assert set(lines2) == set([line4])


def test_it_iters_over_obj_connected_to_this():
    obj1 = Object(obj_id='1')
    obj2 = Object(obj_id='2')
    obj3 = Object(
        obj_id='3',
        connections=[
            Connection(handle=0, to_id='1'),
        ]
    )
    layer = Layer([
        obj1,
        obj2,
        obj3,
    ])
    diagram = Diagram([layer])
    objs = expression.connected_to_this()(obj1)
    assert set(objs) == set([obj3])

    objs2 = expression.connected_to_this()(obj2)
    assert set(objs2) == set()


def test_it_iterates_by_type():
    obj1 = Object(obj_id='1', obj_type='X')
    obj2 = Object(obj_id='2', obj_type='Y')
    obj3 = Object(
        obj_id='3',
        connections=[
            Connection(handle=0, to_id='1'),
        ]
    )
    layer = Layer([
        obj1,
        obj2,
        obj3,
    ])
    diagram = Diagram([layer])
    expr = expression.has_type('X')
    assert set(expr(obj1)) == set([obj1])
    assert set(expr(obj2)) == set()


def test_it_iterates_by_nested_type():
    obj1 = Object(obj_id='1', obj_type='X')
    obj2 = Object(obj_id='2', obj_type='Y')
    obj3 = Object(
        obj_id='3',
        obj_type='X',
        connections=[
            Connection(handle=0, to_id='1'),
        ]
    )
    layer = Layer([
        obj1,
        obj2,
        obj3,
    ])
    diagram = Diagram([layer])
    expr = expression.all(
        expression.has_type('X')
    )
    objs = expr(diagram.objects)
    assert set(objs) == set([obj1, obj3])


def test_it_returns_first_by_type():
    obj1 = Object(obj_id='1', obj_type='X')
    obj2 = Object(obj_id='2', obj_type='Y')
    obj3 = Object(
        obj_id='3',
        obj_type='X',
        connections=[
            Connection(handle=0, to_id='1'),
        ]
    )
    layer = Layer([
        obj1,
        obj2,
        obj3,
    ])
    diagram = Diagram([layer])
    expr = expression.first(
        expression.all(
            expression.has_type('X')
        )
    )
    objs = expr(diagram.objects)
    assert set(objs) == set([obj1])


def test_it_finds_objects_connected_to_given_object_via_lines():
    obj1 = Object(obj_id='1')
    obj2 = Object(obj_id='2')
    obj3 = Object(obj_id='3')
    obj4 = Object(obj_id='4')
    obj5 = Object(obj_id='5')
    line1 = make_straight_line(obj2, obj1)
    line2 = make_straight_line(obj3, obj1)
    line3 = make_straight_line(obj4, obj1)
    line4 = make_straight_line(obj5, obj1)
    layer = Layer([
        obj1,
        obj2,
        obj3,
        obj4,
        obj5,
        line1,
        line2,
        line3,
        line4,
    ])
    diagram = Diagram([layer])
    expr = expression.connected_to_this(
        expression.line_connected_from()
    )
    objs = expr(obj1)
    assert set(objs) == set([obj2, obj3, obj4, obj5])


def test_it_finds_objects_connected_via_lines_two_steps_away():
    obj1 = Object(obj_id='1')
    obj2 = Object(obj_id='2')
    obj3 = Object(obj_id='3')
    obj4 = Object(obj_id='4')
    obj5 = Object(obj_id='5')
    line1 = make_straight_line(obj2, obj1)
    line2 = make_straight_line(obj3, obj1)
    line3 = make_straight_line(obj4, obj1)
    line4 = make_straight_line(obj5, obj4)
    layer = Layer([
        obj1,
        obj2,
        obj3,
        obj4,
        obj5,
        line1,
        line2,
        line3,
        line4,
    ])
    diagram = Diagram([layer])
    expr = expression.inbound_lines(
        expression.line_connected_from(
            expression.inbound_lines(
                expression.line_connected_from()
            )
        )
    )
    objs = expr(obj1)
    assert set(objs) == set([obj5])


def test_it_finds_path_connecting_objects_via_lines_two_steps_away():
    obj1 = Object(obj_id='1')
    obj2 = Object(obj_id='2')
    obj3 = Object(obj_id='3')
    obj4 = Object(obj_id='4')
    obj5 = Object(obj_id='5')
    obj6 = Object(obj_id='6')
    line1 = make_straight_line(obj2, obj1)
    line2 = make_straight_line(obj3, obj1)
    line3 = make_straight_line(obj4, obj1)
    line4 = make_straight_line(obj5, obj4)
    line5 = make_straight_line(obj6, obj4)
    layer = Layer([
        obj1,
        obj2,
        obj3,
        obj4,
        obj5,
        obj6,
        line1,
        line2,
        line3,
        line4,
        line5,
    ])
    diagram = Diagram([layer])
    expr = expression.inbound_lines(
        expression.line_connected_from(
            expression.combine(
                expression.inbound_lines(
                    expression.line_connected_from()
                )
            )
        )
    )
    objs = expr(obj1)
    assert set(objs) == set([
        (obj4, obj5),
        (obj4, obj6),
    ])
