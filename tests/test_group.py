
import site
site.addsitedir('src')

from dia_parser import Group, Object, Layer

def test_group_iterates_all_objects():
    layer = Layer()
    group1 = Group()
    group2 = Group()
    obj1 = Object(layer)
    obj2 = Object(layer)
    obj3 = Object(layer)

    group1.children = [
        obj1,
        obj2,
        group2,
    ]
    group2.children = [
        obj3,
    ]

    assert list(group1.iter_objects()) == [obj1, obj2, obj3]
