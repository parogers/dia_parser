
def noop(obj):
    yield obj

def outbound_lines(expr=noop):
    def matches(obj):
        for line in obj.outbound_lines:
            yield from expr(line)

    return matches

def line_connected_to(expr=noop):
    def matches(obj):
        if obj.is_line:
            yield from expr(obj.as_line.connected_to)

    return matches

def connected_to_this(expr):
    def matches(obj):
        for other in obj.connected_to_this:
            yield from expr(other)

    return matches

def combine(expr):
    def matches(obj):
        for new_obj in expr(obj):
            yield (obj, new_obj)

    return matches

def has_type(type):
    def matches(obj):
        if obj.type == type:
            yield obj

    return matches

