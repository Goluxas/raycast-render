"""
If needed, the *_ip functions can be easily optimized
ip = in-place = the function will change the object itself instead of returning a new instance
"""
# This makes it possible to type hint a class function with its own type
from __future__ import annotations
import math

from pyglet import shapes


class Vector:
    def __init__(self, x: float, y: float = None):
        if y is None:
            assert (
                type(x) is tuple
            ), f"Vector initialized with unknown single argument: {x}"
            self.x = x[0]
            self.y = x[1]
        else:
            self.x: float = x
            self.y: float = y

        self._set_properties()

    def _set_properties(self):
        magnitude: float = math.sqrt(self.x * self.x + self.y * self.y)
        self.magnitude = magnitude

    def rotate(self, angle: float) -> Vector:
        new_x = self.x * math.cos(angle) - self.y * math.sin(angle)
        new_y = self.x * math.sin(angle) + self.y * math.cos(angle)

        return Vector(new_x, new_y)

    def rotate_ip(self, angle: float) -> None:
        new_me = self.rotate(angle)  # holy shit does this work? kinda scary
        self.x = new_me.x
        self.y = new_me.y

    def distance(self, other):
        if isinstance(other, Vector):
            return math.dist((self.x, self.y), (other.x, other.y))
        else:
            return math.dist((self.x, self.y), other)

    def intersects_at(self, line: Line) -> Vector:
        """
        Returns a vector of this point's intersection with the line, if it exists
        ZeroDivisionError occurs if the ray is parallel to the line.
        """
        try:
            t_star: float = -line.c / (line.a * self.x + line.b * self.y)
        except ZeroDivisionError:
            # ray is parallel to line?
            return None
        return Vector(self.x * t_star, self.y * t_star)

    def intersects_which(self, lines: list[Line]) -> Line:
        """
        Checks if there's an intersection in a list of lines. Returns the first line that intersects.
        """
        for line in lines:
            if self.intersects_segment(line):
                return line

        return None

    def intersects_segment(self, line: Line) -> bool:
        intersection = self.intersects_at(line)
        if not intersection:
            return False

        if line.contains_point(intersection):
            return True
        else:
            return False

    def dot_product(self: Vector, vectorB: Vector, angle: float) -> float:
        product: float = self.magnitude * vectorB.magnitude * math.cos(angle)
        return product

    def __add__(self, other):
        if isinstance(other, Vector):
            return Vector(self.x + other.x, self.y + other.y)
        else:
            return Vector(self.x + other[0], self.y + other[1])

    def __sub__(self, other):
        if isinstance(other, Vector):
            return Vector(self.x - other.x, self.y - other.y)
        elif other is (float, float):
            return Vector(self.x - other[0], self.y - other[1])
        else:
            raise NotImplementedError

    def __neg__(self):
        return Vector(-self.x, -self.y)


class Line:
    width = 3
    color = (255, 255, 255)

    def __init__(self, vertexA: Vector, vertexB: Vector):
        if issubclass(type(vertexA), tuple):
            vertexA = Vector(vertexA)
        if issubclass(type(vertexB), tuple):
            vertexB = Vector(vertexB)

        self.vertexA: Vector = vertexA
        self.vertexB: Vector = vertexB
        self._set_line_equation()
        self._set_slope()

    def _set_line_equation(self):
        # General Form of a Line: ax + by + c = 0
        self.a: float = self.vertexA.y - self.vertexB.y
        self.b: float = self.vertexB.x - self.vertexA.x
        self.c: float = (
            self.vertexA.x * self.vertexB.y - self.vertexB.x * self.vertexA.y
        )

    def _set_slope(self):
        """
        Sets the slope, or sets to None if vertical
        """
        if self.b == 0:
            self.slope = None
        else:
            self.slope: float = -self.a / self.b

    def offset(self, vector: Vector) -> Line:
        new_A = self.vertexA + vector
        new_B = self.vertexB + vector
        return Line(new_A, new_B)

    def offset_ip(self, vector: Vector) -> None:
        new_me = self.offset(vector)
        self.vertexA = new_me.vertexA
        self.vertexB = new_me.vertexB

    def contains_point(self, point: Vector) -> bool:
        # x between endpoint x values
        if self.vertexA.x <= self.vertexB.x:
            if self.vertexA.x <= point.x <= self.vertexB.x:
                # could be contained
                ...
            else:
                return False
        else:
            if self.vertexB.x <= point.x <= self.vertexA.x:
                # could be contained
                ...
            else:
                return False

        # y between endpoint y values
        if self.vertexA.y <= self.vertexB.y:
            if self.vertexA.y <= point.y <= self.vertexB.y:
                # could be contained
                ...
            else:
                return False
        else:
            if self.vertexB.y <= point.y <= self.vertexA.y:
                # could be contained
                ...
            else:
                return False

        # (Bx - Ax)(py - Ay) = (px - Ax)(By - Ay)
        slope_a = (self.vertexB.x - self.vertexA.x) * (point.y - self.vertexA.y)
        slope_b = (point.x - self.vertexA.x) * (self.vertexB.y - self.vertexA.y)
        if math.isclose(slope_a, slope_b):
            # could be contained
            ...
        else:
            return False

        # If it passed the above tests then it is contained
        return True

    def angle_between_lines(self, lineB: Line) -> float:
        # See notebook for how this was derived
        angle: float = math.atan(
            abs((lineB.slope - self.slope) / (1 + self.slope * lineB.slope))
        )
        return angle

    def complex_contains_point(self, point: Vector) -> bool:
        line_AP = Line(self.vertexA, point)
        angle = self.angle_between_lines(line_AP)
        if not (
            math.isclose(angle, 0.0, abs_tol=1e-14) or math.isclose(angle, math.pi)
        ):
            return False

        own_magnitude = self.vertexA.dot_product(self.vertexB, angle)
        test_magnitude = self.vertexA.dot_product(point, angle)

        if test_magnitude >= 0 and test_magnitude <= own_magnitude:
            return True

    def init_render(self, game):
        self.repr = shapes.Line(
            self.vertexA.x,
            self.vertexA.y,
            self.vertexB.x,
            self.vertexB.y,
            width=self.width,
            color=self.color,
            batch=game.batch,
        )