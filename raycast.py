import math

class Vector():
    def __init__(self, x, y):
        self.x: float = x
        self.y: float = y
        self._set_properties()

    def _set_properties(self):
        magnitude: float = math.sqrt(self.x * self.x + self.y * self.y)
        self.magnitude = magnitude

    def rotate(self, angle: float):
        new_x = self.x * math.cos(angle) - self.y * math.sin(angle)
        new_y = self.x * math.sin(angle) + self.y * math.cos(angle)

        return Vector(new_x, new_y)

    def distance(self, other):
        if isinstance(other, Vector):
            return math.dist((self.x, self.y), (other.x, other.y))
        else:
            return math.dist((self.x, self.y), other)
    
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

class Line():
    def __init__(self, vertexA: Vector, vertexB: Vector):
        self.vertexA: Vector = vertexA
        self.vertexB: Vector = vertexB
        self._set_line_equation()
        self._set_slope()

    def _set_line_equation(self):
        # General Form of a Line: ax + by + c = 0
        self.a: float = self.vertexA.y - self.vertexB.y
        self.b: float = self.vertexB.x - self.vertexA.x
        self.c: float = self.vertexA.x * self.vertexB.y - self.vertexB.x * self.vertexA.y

    def _set_slope(self):
        self.slope: float = -self.a / self.b

    def offset(self, vector: Vector):
        new_A = self.vertexA + vector
        new_B = self.vertexB + vector
        return Line(new_A, new_B)

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


    def complex_contains_point(self, point: Vector) -> bool:
        line = Line(self.vertexA, point)
        angle = angle_between_lines(self, line)
        if not (math.isclose(angle, 0.0, abs_tol=1e-14) or math.isclose(angle, math.pi)):
            return False

        own_magnitude = dot_product(self.vertexA, self.vertexB, angle)
        test_magnitude = dot_product(self.vertexA, point, angle)

        if test_magnitude >= 0 and test_magnitude <= own_magnitude:
            return True

def find_intersect(ray: Vector, line: Line) -> Vector:
    t_star: float = - line.c / (line.a * ray.x + line.b * ray.y)
    return Vector(ray.x * t_star, ray.y * t_star)

def angle_between_lines(lineA: Line, lineB: Line) -> float:
    angle: float = math.atan(abs((lineB.slope - lineA.slope) / (1 + lineA.slope * lineB.slope)))
    return angle

def dot_product(vectorA: Vector, vectorB: Vector, angle: float) -> float:
    product: float = vectorA.magnitude * vectorB.magnitude * math.cos(angle)
    return product

def intersects(ray: Vector, line: Line) -> bool:
    try:
        intersection = find_intersect(ray, line)
    except ZeroDivisionError:
        return False
    if line.contains_point(intersection):
        #return True
        # value max 9 min 1
        # 9 at 1 or less
        # 1 at 10 or more
        distance = intersection.distance((0,0))
        if distance <= 1:
            value = 9
        elif distance >= 10:
            value = 1
        else:
            """
            factor = 9/9ths of 9 at distance 1, 1/9th of 9 at distance 10
            height is inversely proprotional to distance
            y = mx+b
            h = md+b
            line from (1,9) to (10,1), m = 1-9 / 10-1 = -8/9
            intersect = 9 = (-8/9)(1) + b, 9 = -8/9 + b, b = 9+8/9 = 89/9
            intersect = 1 = (-8/9)(10) + b, 1 = -80/9 + b, b = 9/9 + 80/9 = 89/9
            """
            value = (-8.0/9) * distance + (89.0/9)
            value = math.floor(value)
        return str(value)
    else:
        return False

def render(player, direction, fov, environment, horizontal_resolution):
    wall = environment.offset(-player)
    starting_view_vector = direction.rotate(fov/2)
    d_theta = fov/horizontal_resolution

    out = ""

    for i in range(horizontal_resolution):
        view_vector = starting_view_vector.rotate(-d_theta*i)
        value = intersects(view_vector, wall)
        if value:
            out += value
        else:
            out += "."

    print(out)

if __name__ == '__main__':
    player = Vector(0, 0)
    direction = Vector(0.5, 0.5)
    fov: float = math.pi / 2 # 90 degrees
    wall = Line(Vector(1,5), Vector(5,1))
    resolution = 100

    # move player around the wall widely
    time_per_action = 5
    d_theta = (-math.pi / 2) / time_per_action # -90 degrees = turn right 90 degrees
    d_pos = 7 / time_per_action # since we're moving straight vertical/horizontal this is easy
    
    # 0, 0 -> 0, 7
    for dt in range(time_per_action):
        render(player, direction, fov, wall, resolution)
        player = player + (0, d_pos)
    print("Walked North")
    # rotate view 90 degrees right
    for dt in range(time_per_action):
        render(player, direction, fov, wall, resolution)
        direction = direction.rotate(d_theta)
    print("Turned right")
    # 0, 7 -> 7, 7
    for dt in range(time_per_action):
        render(player, direction, fov, wall, resolution)
        player = player + (d_pos, 0)
    print("Walked East")
    # rotate view 90 degrees right
    for dt in range(time_per_action):
        render(player, direction, fov, wall, resolution)
        direction = direction.rotate(d_theta)
    print("Turned right")
    # 7, 7 -> 7, 0
    for dt in range(time_per_action):
        render(player, direction, fov, wall, resolution)
        player = player + (0, -d_pos)
    print("Walked South")
    # rotate view 90 degrees right
    for dt in range(time_per_action):
        render(player, direction, fov, wall, resolution)
        direction = direction.rotate(d_theta)
    print("Turned right")

        
        

    """
    # simulate turning left over time
    # let's say, turn 90 degrees left in 20 frames
    total_turn = math.pi / 2
    frames = 20
    turn_per_frame = total_turn / frames
    for i in range(frames):
        cur_dir = direction.rotate(turn_per_frame * i)
        render(cur_dir, fov, wall, steps)
    """