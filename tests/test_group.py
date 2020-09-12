
import site
site.addsitedir('src')

from dia_parser import Group, Object, Layer

def test_group_iterates_all_objects():
    obj1 = Object()
    obj2 = Object()
    obj3 = Object()
    group = Group([
        obj1,
        obj2,
        Group([
            obj3,
        ])
    ])

    assert list(group.iter_objects()) == [obj1, obj2, obj3]

def test_it_assigns_the_parent_node():
    obj1 = Object()
    obj2 = Object()
    obj3 = Object()
    group2 = Group([
        obj3,
    ])
    group1 = Group([
        obj1,
        obj2,
        group2,
    ])

    assert obj1.parent == group1
    assert obj2.parent == group1
    assert group2.parent == group1
    assert obj3.parent == group2
