from objects import Vector, Line


def test_vector_intersection_with_line_returns_None_if_parallel_vertical():
    ray = Vector(0, 1)  # points straight up
    line = Line(Vector(1, 0), Vector(1, 1))  # also straight up, 1 x over

    result = ray.intersects_at(line)

    assert result is None


def test_vector_intersection_with_line_returns_None_if_parallel_diagonal():
    ray = Vector(1, 1)  # points NE
    line = Line(Vector(1, 0), Vector(2, 1))  # also NE

    result = ray.intersects_at(line)

    assert result is None


def test_vector_intersection_with_line_returns_intersection_point_even_near_parallel():
    """
    How do I make something near parallel?
    Rotate parallel just a tiny fraction of a radian?
    What's the min value of a float? (2.2...e-308, holy fuck)
    """
    ray = Vector(0, 1)  # points N
    line = Line(Vector(1, 0), Vector(1, 1))  # also N

    # math functions round their results to 1.0 if you go smaller than about e-7
    ray.rotate_ip(1e-7)

    result = ray.intersects_at(line)

    # there's probably more specific values i need to check, but maybe i offload that to
    # the tests for the intersects_at function (that I'll probably never write)
    assert result is not None
