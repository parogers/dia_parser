
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
